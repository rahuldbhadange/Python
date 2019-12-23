# Copyright (c) 2018 Rolls-Royce Power Systems AG. All rights reserved.

import logging
import json
from hashlib import md5 as hashlib_md5
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor
from base64 import b64decode
from binascii import Error as binascii_Error

import requests

from IoticAgent import ThingRunner

from ioticlabs.dt.api.integrator import (
    Integrator, IntegratorCallbacks, T2ProviderFailureReason,
    EventPublishFailure, AssetUnknown
)
from ioticlabs.dt.api.util import log_exceptions, NestedConfig
from ioticlabs.dt.common.util import non_empty_str, non_negative_int

from ioticlabs.dt.common.item_cache import get_cache

from rrps.dt.events.t2defs import T2_REQUEST_TALEND_DOCUMENT

from rrps.dt.events import TalendTimDocumentSet

from . import mockpdf

log = logging.getLogger(__name__)

MOCK_DATA_FILE = 'data/mock-data.json'

TalendConfig = namedtuple('TalendConfig', 'endpoint endpoint_single usr pwd timeout')


class TalendTimDocumentIntegrator(IntegratorCallbacks, ThingRunner):
    """ TalendTimDocumentIntegrator initializing """

    def __init__(self, config, agent_config):

        super().__init__(config=agent_config)

        if not (isinstance(config, dict) and all(section in config for section in ('integrator', 'config'))):
            raise ValueError('Configuration invalid / missing required section')

        # Whilst the integrator core requires particular configuration, top-level sections could be defined to provide
        # parameters specific to this integrator.
        self.__integrator = Integrator(config['integrator'], self.client, self)
        self.__assets = set()
        self.__config = config
        # data cache used to check that the asset has been changed or not before publishing the event
        self.__data_cache = get_cache(config, config_path='integrator.asset.cache.method')
        self.__use_mock_data = NestedConfig.get(self.__config, 'config.use_mock_data', required=False, default=False)
        self.__workers = NestedConfig.get(self.__config,
                                          'config.workers', required=False, default=1, check=non_negative_int)
        self.__loop_time = NestedConfig.get(self.__config,
                                            'config.loop_time', required=False, default=5, check=non_negative_int)

        self.__req_pool = ThreadPoolExecutor(max_workers=self.__workers)

        self.__talend_config_info = TalendConfig(
            endpoint=NestedConfig.get(self.__config,
                                      'config.talend.endpoint', required=True, check=non_empty_str),
            endpoint_single=NestedConfig.get(self.__config,
                                             'config.talend.endpoint_single', required=True, check=non_empty_str),
            usr=NestedConfig.get(self.__config, 'config.talend.usr', required=True, check=non_empty_str),
            pwd=NestedConfig.get(self.__config, 'config.talend.pwd', required=True, check=non_empty_str),
            timeout=int(NestedConfig.get(self.__config,
                                         'config.talend.timeout', required=False, default=10, check=non_negative_int))
        )

    def on_startup(self):
        """ Starts the integrator. Other public methods herein must not be called beforehand.
        Should be called after starting Iotic agent.
        Alternatively use with keyword on the instance. """
        log.info('Talend Tim Document Integrator Startup')
        self.__data_cache.start()
        self.__integrator.start()

    def main(self):
        """ Talend Tim Document Integrator Started Running """
        log.info('Talend Tim Document Integrator Running')
        self.__process_data()
        loop_time = self.__loop_time
        while not self.wait_for_shutdown(loop_time):
            self.__process_data()

    def on_shutdown(self, exc_info):
        """ Stops the integrator. Should be called before shutting down the Iotic agent. """
        log.info('Talend Tim Document Integrator Shutdown')
        self.__integrator.stop()
        self.__data_cache.stop()

    # for IntegratorCallbacks
    def on_asset_created(self, asset_id):
        """ A new asset has been created.
        Called once for each known asset on startup as well as whenever
        a new asset appears whilst the integrator is running. """
        log.info('Asset created: %s', asset_id)
        self.__assets.add(asset_id)

    # for IntegratorCallbacks
    def on_asset_deleted(self, asset_id):
        """ An asset has been deleted.
        Called whenever an asset has been removed and should no longer be considered by the integrator.
        Note: This is NOT called if an asset has been deleted whilst the integrator is not running. """
        log.info('Asset deleted: %s', asset_id)
        self.__assets.discard(asset_id)

    # for IntegratorCallbacks
    def on_t2_request(self, request):
        """ A new type2 request has been made for a particular asset.
        request - instance of T2Request """
        self.__req_pool.submit(self.__process_t2, request)

    # Wrap since run via thread pool without handling return/exception
    @log_exceptions(log)
    def __process_t2(self, request):
        """ processing t2 request """
        log.info('New T2 req for %s - %s(%r)', request.asset_id, request.type_, request.data)

        if request.type_ != T2_REQUEST_TALEND_DOCUMENT:
            log.warning('Ignoring unknown request type %s', request.type_)
            return
        self.__t2_do_tlddoc(request)

    def __t2_do_tlddoc(self, request):
        decoded = json.loads(request.data.decode('utf-8'))
        data = self.__get_tim_doc(decoded["serialNumber"], decoded["documentLabel"], decoded["documentName"])
        if data:
            try:
                self.__integrator.t2_respond(request, "application/pdf", b64decode(data))
            except binascii_Error:
                log.error("Failed to b64decode data")
                self.__integrator.t2_respond_error(request, T2ProviderFailureReason.REQ_UNHANDLED)
        else:
            self.__integrator.t2_respond_error(request, T2ProviderFailureReason.REQ_UNHANDLED)

    def __get_tim_doc(self, serial_no, document_label, document_name):
        log.info("Get Talend doc for: %s", serial_no)

        data = None
        try:
            if self.__use_mock_data == 1:
                return mockpdf.data
        except ValueError as ex:
            log.error(ex)

        endpoint = self.__talend_config_info.endpoint_single.\
            format(asset_id=serial_no, doc_label=document_label, doc_name=document_name)
        usr = self.__talend_config_info.usr
        pwd = self.__talend_config_info.pwd
        timeout = self.__talend_config_info.timeout

        log.debug("Calling: %s", endpoint)

        try:
            resp = requests.get(endpoint, auth=(usr, pwd), verify=False, timeout=timeout)
            log.debug("Response status: %s", resp.status_code)
            if resp.text and resp.status_code == requests.codes['ok']:
                try:
                    data = resp.json()['document']
                except Exception as ex:  # pylint: disable=broad-except
                    log.error("Could not parse JSON from response: %s", resp.text)
                    log.error(ex)
        except requests.exceptions.RequestException as ex:
            log.error(ex)

        return data

    def __get_data_for_asset(self, asset_id):
        """ returns Talend data for asset_id """
        log.info("Get Talend data for: %s", asset_id)

        data = None

        if self.__use_mock_data == 1:
            log.debug("Using mock data")
            with open(MOCK_DATA_FILE, mode="r", encoding="utf-8") as f:
                data = json.load(f)

        else:
            # asset_id hack for RR Dev environment
            # The dev environment TalendTimDocument API uses a specific asset_id we will swap two of our test IDs.
            if asset_id in ('1000021', '1000015'):
                asset_id = '16701003340'

            usr = self.__talend_config_info.usr
            pwd = self.__talend_config_info.pwd
            endpoint = self.__talend_config_info.endpoint_single.format(asset_id=asset_id)
            timeout = self.__talend_config_info.timeout

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

    def __process_data(self):
        """ Processing Talend Tim Documents """
        log.info("Processing Talend Tim Documents")
        for asset_id in list(self.__assets):
            log.debug("Processing asset: %s", asset_id)
            data = self.__get_data_for_asset(asset_id)
            if data and self.__has_asset_data_changed_for(asset_id, data):
                event = TalendTimDocumentSet(asset_id, data=data["documentList"])
                log.debug("Publishing event: %s", event)

                try:
                    self.__integrator.publish_event(event)
                    self.__cache_asset_data_for(asset_id, data)

                # These will all retry
                except EventPublishFailure as ex:
                    log.error("Event Publish Failure: %s", ex)
                except AssetUnknown:
                    pass

    # Checks to see if the given data for the asset has changed
    # since it was last processed.
    def __has_asset_data_changed_for(self, asset_id, data):
        """ Checking wheather asset cache data has changed for asset_id or not """
        log.info("Checking asset cache for: %s", asset_id)
        try:
            asset_id_hash = self.__data_cache.get_attr(asset_id, 'hash')
        except KeyError:
            # No cache so this is new data
            return True

        data_hash = self.__compute_data_hash(data)

        if asset_id_hash['hash'] != data_hash:
            # data has changed
            return True
        # Nothing has changed for this data
        return False

    @classmethod
    def __compute_data_hash(cls, data):
        """ computing data"""
        jdata = json.dumps(data, sort_keys=True, separators=(',', ':'))
        return hashlib_md5(jdata.encode('utf8')).hexdigest()

    # After publishing the event, update the cache
    def __cache_asset_data_for(self, asset_id, data):
        """ updating Cache asset data for asset_id """
        log.info("Cache asset for: %s", asset_id)
        data_hash = self.__compute_data_hash(data)
        self.__data_cache.mark_as_known(asset_id, hash=data_hash)
