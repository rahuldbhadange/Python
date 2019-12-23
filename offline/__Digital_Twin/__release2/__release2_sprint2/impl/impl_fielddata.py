# Copyright (c) 2018 Rolls-Royce Power Systems AG. All rights reserved.

from time import monotonic
import logging
import os
from io import StringIO
from csv import DictReader
from functools import partial

from azure.storage.blob import BlockBlobService

from IoticAgent import ThingRunner
from IoticAgent.IOT import Client

from ioticlabs.dt.api.integrator import EventPublishFailure
from ioticlabs.dt.api.integrator import AssetUnknown
from rrps.dt.api.fielddata.integrator import FdIntegrator, FdIntegratorCallbacks
from rrps.dt.events import FieldDataSuccessSet, FieldDataErrorSet

from rrps.dt.api.fielddata.values import Sample

from .Asset import Asset

log = logging.getLogger(__name__)

# The terminator used in CSV files stored in Azure blobs.
CSV_TERMINATOR = '\r\n'


class _InvalidFieldBlobFormat(Exception):
    """Used to report unexpected header / trailing data in field data blob"""
    pass


class FieldDataIntegrator(FdIntegratorCallbacks, ThingRunner):

    def __init__(self, config, agent_config, fd_agent_config=None):
        super().__init__(config=agent_config)

        if not (
                isinstance(config, dict) and
                all(section in config for section in (
                    'integrator', 'fielddata', 'config'))
        ):
            raise ValueError(
                'Configuration invalid / missing required section')

        if fd_agent_config:
            self.__fd_client = Client(config=fd_agent_config)
        else:
            self.__fd_client = None

        # Whilst the integrator core requires particular configuration, top-level sections could be defined to provide
        # parameters specific to this integrator.
        self.__integrator = FdIntegrator(
            config['integrator'], config['fielddata'], self.client, self, fd_client=self.__fd_client
        )
        self.__assets = {}
        self.__config = config

        blob_account_name = self.__config['config']['azure']['blob_account_name']
        blob_account_key = self.__config['config']['azure']['blob_account_key']

        self.__block_blob_service = BlockBlobService(account_name=blob_account_name, account_key=blob_account_key)

        self.BLOB_CACHE_DIR = self.__config['config']['azure'].get('blob_cache_dir',
                                                                   os.path.join('cfg', 'tmpdata', 'data-cache'))
        if not os.path.exists(self.BLOB_CACHE_DIR):
            log.debug("Creating blob cache dir")
            os.makedirs(self.BLOB_CACHE_DIR, exist_ok=True)


    def on_startup(self):
        log.debug('Field Data Integrator Startup')
        if self.__fd_client:
            self.__fd_client.start()
        self.__integrator.start()

    def main(self):
        log.debug('Field Data Integrator Running')

        while True:
            start = monotonic()
            # TODO - at this point no assets might be known locally yet. This means the first process pass might do
            # nothing and then one has to wait e.g. 600s before processing actually happens.
            self.__process_data()
            stop = monotonic()
            loop_timer = self.__config['config']['loop_timer']

            if self.wait_for_shutdown(max(0, loop_timer - (stop - start))):
                break

    def on_shutdown(self, exc_info):
        log.debug('Field Data Integrator Shutdown')
        self.__integrator.stop()
        if self.__fd_client:
            self.__fd_client.stop()

    # for FdIntegratorCallbacks
    def on_asset_created(self, asset_id):
        log.debug('Asset created: %s', asset_id)
        asset = Asset(asset_id, partial(self.__publish_fielddata_for,
                                        asset_id), self.__config['config']['row_limit'])
        self.__assets[asset_id] = asset

    # for FdIntegratorCallbacks
    def on_asset_deleted(self, asset_id):
        log.debug('Asset deleted: %s', asset_id)
        self.__assets.pop(asset_id, None)

    # for IntegratorCallbacks
    def on_t2_request(self, request):
        pass

    @staticmethod
    def __get_fname_from_blobname(blobname):
        return blobname.split('/')[-1]

    @staticmethod
    def __get_date_from_blobname(blobname):
        return blobname[0:blobname.rindex('/')]

    @staticmethod
    def __get_asset_id_from_blobname(blobname):
        prefix = "_".join(blobname.split("_", 2)[:2]) if blobname.startswith(
            "DPU") else blobname.split('_')[0]
        return prefix.split('/')[-1]

    def __process_data(self):
        blob_container_name = self.__config['config']['azure']['blob_container_name']
        generator = self.__block_blob_service.list_blobs(blob_container_name)

        log.info("starting to process blobs")
        for blob in generator:
            blobname = blob.name
            asset_id = self.__get_asset_id_from_blobname(blobname)

            if asset_id in self.__assets:
                asset = self.__assets[asset_id]
                fname = self.__get_fname_from_blobname(blobname)

                if self.__fname_is_new(fname):
                    if asset.new_to_me(fname):
                        log.info("Processing %s", fname)
                        errors = self.__process_blob_for(asset, blob)

                        data = {"Blobname": blobname}
                        self.__publish_success(asset.asset_id, data)

                        if errors:
                            self.__publish_errors(asset.asset_id,
                                                  [{"Blobname": blobname, "Error": error} for error in errors])

                        asset.last_fname = fname
                        self.__remember_fname(fname)
                else:
                    log.debug("fname %s already seen. Skipping", fname)

    def __publish_success(self, asset, data):
        event = FieldDataSuccessSet(asset, data=data)
        log.info("Publish success event: %s Asset: %s", event, asset)

        try:
            self.__integrator.publish_event(event)

        # These will all retry
        except EventPublishFailure as ex:
            log.error("Event Publish Failure: %s", ex)
        except AssetUnknown as ex:
            pass

    def __publish_errors(self, asset, errors):
        event = FieldDataErrorSet(asset, data=errors)
        log.info("Publish error event: %s Asset: %s", event, asset)

        try:
            self.__integrator.publish_event(event)

        # These will all retry
        except EventPublishFailure as ex:
            log.error("Event Publish Failure: %s", ex)
        except AssetUnknown as ex:
            pass

    # Save the fname so we don't parse it again

    def __remember_fname(self, fname):
        log.debug("Caching fname: %s", fname)
        file_path = os.path.join(self.BLOB_CACHE_DIR, fname)

        # Just create a file
        f = open(file_path, "w+")
        f.close()

    # Check if the given fname has been seen/processed before
    def __fname_is_new(self, fname):
        log.debug("Checking fname cache for: %s", fname)
        file_path = os.path.join(self.BLOB_CACHE_DIR, fname)

        if not os.path.isfile(file_path):
            # We've not seen this file before
            return True

        # We've seen this before
        return False

    # Used by Asset instances to share field data
    def __publish_fielddata_for(self, asset_id, template, time):
        self.__integrator.publish_fielddata(Sample(asset_id, template, time))

    def __process_blob_for(self, asset, blob):
        """Get the blob as a stream.c
        Parse the blob
        send the blob to asset share feed
        """
        # Could use get_blob_to_stream. However, instead of writing data directly to this stream, it first saves it
        # to a bytes object anyway. As such there is no advantage of using it currently!

        blob_container_name = self.__config['config']['azure']['blob_container_name']

        blob_data = self.__block_blob_service.get_blob_to_text(blob_container_name, blob.name, encoding='utf8')

        errors = asset.share_rows(
            self.__rows_from_fielddata_stream(StringIO(blob_data.content)))
        asset.last_fname = blob.name

        return errors

    @staticmethod
    def __rows_from_fielddata_stream(stream):
        """Expects file-like object which supports readline() in text mode. Returns iterable of rows (as mappings) or
        raises InvalidFieldData if header could not be parsed."""
        if 'UXX-BEGIN' not in stream.readline():
            raise _InvalidFieldBlobFormat('File header missing')

        line = stream.readline()
        while 'UXX-END' not in line:
            if not line:  # end of file reached
                raise _InvalidFieldBlobFormat('File header terminator missing')
            line = stream.readline()

        headers = stream.readline()[:-len(CSV_TERMINATOR)].split(';')  # Heading line is next
        stream.readline()  # this has units
        stream.readline()  # this has datatypes

        return iter(DictReader(stream, delimiter=';', lineterminator=CSV_TERMINATOR, fieldnames=headers))
