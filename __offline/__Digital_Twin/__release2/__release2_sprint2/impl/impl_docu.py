# Copyright (c) 2018 Rolls-Royce Power Systems AG. All rights reserved.

import logging
import json
import os
from hashlib import md5 as hashlib_md5
from concurrent.futures import ThreadPoolExecutor
from base64 import b64decode
from binascii import Error as binascii_Error

import requests

from IoticAgent import ThingRunner

from ioticlabs.dt.api.integrator import Integrator, IntegratorCallbacks, T2ProviderFailureReason
from ioticlabs.dt.api.integrator import EventPublishFailure
from ioticlabs.dt.api.integrator import AssetUnknown

from ioticlabs.dt.api.util import log_exceptions
from ioticlabs.dt.api.util import NestedConfig

from rrps.dt.events.t2defs import T2_REQUEST_TALEND_DOCUMENT

from rrps.dt.events import TalendTimDocumentSet

from . import mockpdf


log = logging.getLogger(__name__)


class TalendTimDocumentIntegrator(IntegratorCallbacks, ThingRunner):

    def __init__(self, config, agent_config):

        super().__init__(config=agent_config)

        if not (isinstance(config, dict) and all(section in config for section in ('integrator', 'config'))):
            raise ValueError(
                'Configuration invalid / missing required section')

        # Whilst the integrator core requires particular configuration, top-level sections could be defined to provide
        # parameters specific to this integrator.
        self.__integrator = Integrator(config['integrator'], self.client, self)
        self.__assets = set()
        self.__config = config
        self.__data_cache = self.__config['config']['data-cache']
        self.__req_pool = ThreadPoolExecutor(max_workers=self.__config['config']['workers'])

    def on_startup(self):
        log.info('Talend Tim Document Integrator Startup')

        self.__integrator.start()

    def main(self):
        log.info('Talend Tim Document Integrator Running')
        self._process_data()
        loop_time = self.__config['config']['loop_time']
        while not self.wait_for_shutdown(loop_time):
            self._process_data()

    def on_shutdown(self, exc_info):
        log.info('Talend Tim Document  Integrator Shutdown')
        self.__integrator.stop()

    # for IntegratorCallbacks
    def on_asset_created(self, asset_id):
        log.info('Asset created: %s', asset_id)
        self.__assets.add(asset_id)

    # for IntegratorCallbacks
    def on_asset_deleted(self, asset_id):
        log.info('Asset deleted: %s', asset_id)
        self.__assets.discard(asset_id)

    # for IntegratorCallbacks
    def on_t2_request(self, request):
        self.__req_pool.submit(self.__process_t2, request)

    # Wrap since run via thread pool without handling return/exception
    @log_exceptions(log)
    def __process_t2(self, request):
        log.info('New T2 req for %s - %s(%r)', request.asset_id, request.type_, request.data)

        if request.type_ != T2_REQUEST_TALEND_DOCUMENT:
            log.warning('Ignoring unknown request type %s', request.type_)
            return
        self.__t2_do_tlddoc(request)

    def __t2_do_tlddoc(self, request):
        decoded = json.loads(request.data.decode('utf-8'))
        data = self._get_tim_doc(decoded["serialNumber"], decoded["documentLabel"], decoded["documentName"])
        if data:
            try:
                self.__integrator.t2_respond(request, "application/pdf", b64decode(data))
            except binascii_Error:
                log.error("Failed to b64decode data")
                self.__integrator.t2_respond_error(request, T2ProviderFailureReason.REQ_UNHANDLED)
        else:
            self.__integrator.t2_respond_error(request, T2ProviderFailureReason.REQ_UNHANDLED)

    def _get_tim_doc(self, serial_no, document_label, document_name):
        log.info("Get Talend doc for: %s", serial_no)

        data = None

        if self.__config['config']['use_mock_data'] == 1:
            return mockpdf.data

        endpoint = self.__config['config']['talend']['endpoint_single']
        usr = self.__config['config']['talend']['usr']
        pwd = self.__config['config']['talend']['pwd']
        endpoint = endpoint.replace('XXX_ASSET_ID_XXX', serial_no)
        endpoint = endpoint.replace('XXX_DOC_LABEL_XXX', document_label)
        endpoint = endpoint.replace('XXX_DOC_NAME_XXX', document_name)
        timeout = int(self.__config['config']['talend']['timeout'])

        log.debug("Calling: %s", endpoint)

        try:
            resp = requests.get(endpoint, auth=(usr, pwd), verify=False, timeout=timeout)
            log.debug("Response status: %s", resp.status_code)
            if resp.text and resp.status_code == requests.codes['ok']:
                try:
                    data = resp.json()['document']
                except Exception as ex:  # pylint: disable=broad-except
                    log.error("Could not parse JSON from response: %s", resp.text)
        except requests.exceptions.RequestException as ex:
            log.error(ex)

        return data

    def _get_data_for_asset(self, asset_id):
        log.info("Get Talend data for: %s", asset_id)

        data = None

        if self.__config['config']['use_mock_data'] == 1:
            log.debug("Using mock data")
            with open(self.MOCK_DATA_FILE, mode="r", encoding="utf-8") as f:
                data = json.load(f)

        else:
            endpoint = self.__config['config']['talend']['endpoint']
            usr = self.__config['config']['talend']['usr']
            pwd = self.__config['config']['talend']['pwd']

            key = 'config.enable_sap_sample_serial_hack'
            if NestedConfig.get(self.__config, key, required=False, default=False, check=bool):
                if asset_id == '1000021' or asset_id == '1000015':
                    asset_id = '16701003340'

            endpoint = endpoint.replace('XXX_ASSET_ID_XXX', asset_id)
            timeout = int(self.__config['config']['talend']['timeout'])

            log.debug("Calling: %s", endpoint)

            try:
                resp = requests.get(endpoint, auth=(usr, pwd), verify=False, timeout=timeout)
                log.debug("Response status: %s", resp.status_code)
                if resp.text and resp.status_code == requests.codes['ok']:
                    try:
                        data = resp.json()
                    except Exception as ex:
                        log.error("Could not parse JSON from response: %s", resp.text)
                        raise ex
            except requests.exceptions.RequestException as ex:
                log.error(ex)

        return data

    def _process_data(self):
        log.info("Processing Talend Tim Documents")
        for asset_id in list(self.__assets):
            log.debug("Processing asset: %s", asset_id)
            data = self._get_data_for_asset(asset_id)
            if data is not None:
                if self._has_asset_data_changed_for(asset_id, data):
                    event = TalendTimDocumentSet(asset_id, data=data["documentList"])
                    log.debug("Publishing event: %s", event)

                    try:
                        self.__integrator.publish_event(event)
                        self._cache_asset_data_for(asset_id, data)

                    # These will all retry
                    except EventPublishFailure as ex:
                        log.error("Event Publish Failure: %s", ex)
                    except AssetUnknown as ex:
                        pass

    # Checks to see if the given data for the asset has changed
    # since it was last processed.
    def _has_asset_data_changed_for(self, asset_id, data):
        log.info("Checking asset cache for: %s", asset_id)
        if not os.path.exists(self.__data_cache):
            # No cache so this is new data
            return True

        filename = asset_id + '.json'
        file_path = os.path.join(self.__data_cache, filename)

        if not os.path.isfile(file_path):
            # No file exists so this is new data
            return True

        with open(file_path, mode="r", encoding="utf-8") as f:
            cached_data_hash = f.read()

        data_hash = self.__compute_data_hash(data)
        if cached_data_hash != data_hash:
            os.remove(file_path)
            # The data has changed so flush the cache
            return True

        # Nothing has changed for this data
        return False

    @classmethod
    def __compute_data_hash(cls, data):
        jdata = json.dumps(data, sort_keys=True, separators=(',', ':'))
        return hashlib_md5(jdata.encode('utf8')).hexdigest()

    def _cache_asset_data_for(self, asset_id, data):
        log.info("Cache asset for: %s", asset_id)
        if not os.path.exists(self.__data_cache):
            log.debug("Creating data cache")
            os.makedirs(self.__data_cache, exist_ok=True)

        filename = asset_id + '.json'
        file_path = os.path.join(self.__data_cache, filename)

        if not os.path.isfile(file_path):
            with open(file_path, mode="w", encoding="utf-8") as f:
                f.write(self.__compute_data_hash(data))
            log.debug("Caching data for asset %s", asset_id)

    MOCK_DATA_FILE = os.path.join('cfg', 'mock-data.json')
