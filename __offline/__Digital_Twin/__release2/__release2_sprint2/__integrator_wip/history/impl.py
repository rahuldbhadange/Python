# Copyright (c) 2019 Rolls-Royce Power Systems AG. All rights reserved.

import datetime
import logging
import json
from re import search
from binascii import Error as binascii_Error, a2b_base64
from hashlib import md5 as hashlib_md5
from concurrent.futures import ThreadPoolExecutor
from collections import namedtuple
from collections.abc import Mapping
from mimetypes import guess_type
import requests

from IoticAgent import ThingRunner

from ioticlabs.dt.api.integrator import (
    Integrator, IntegratorCallbacks,
    T2ProviderFailureReason, EventPublishFailure, AssetUnknown
)
from ioticlabs.dt.api.util import NestedConfig, log_exceptions
from ioticlabs.dt.common.util import non_empty_str, non_negative_int

from ioticlabs.dt.common.item_cache import get_cache

from rrps.dt.events import (
    SapEquipmentHistoryDeliverySet,
    SapEquipmentHistoryMaintenanceContractSet,
    SapEquipmentHistoryMaterialMovementSet,
    SapEquipmentHistoryInspectionLotSet,
    SapEquipmentHistoryProductionOrderSet,
    SapEquipmentHistoryPhysicalInventorySet,
    SapEquipmentHistoryPurchaseOrderSet,
    SapEquipmentHistoryPmOrderSet,
    SapEquipmentHistoryNotificationSet,
    SapEquipmentHistoryInstallationHistorySet
)
from rrps.dt.events.t2defs import T2_REQUEST_SAP_DOCUMENTSINGLE


log = logging.getLogger(__name__)


MOCK_DATA_FILE = "data/mock-equipment-history-data.json"
MOCK_DOCUMENT_FILE = "data/mock-document-data.json"

SapConfig = namedtuple(
    'SapConfig', 'eq_hist_endp eq_doc_endp eq_doc_single usr pwd timeout'
)


class SAPEquipmentHistoryIntegrator(IntegratorCallbacks, ThingRunner):

    def __init__(self, config, agent_config):
        super().__init__(config=agent_config)

        if not (isinstance(config, Mapping) and
                all(section in config for
                    section in ('integrator', 'config'))):
            raise ValueError(
                'Configuration invalid / missing required section')

        # parameters specific to this integrator.
        self.__integrator = Integrator(config['integrator'], self.client, self)
        self.__assets = set()
        self.__config = config
        # data cache used to check that the asset has been
        # changed or not before publishing the event
        self.__data_cache = get_cache(
            self.__config,
            config_path='integrator.asset.cache.method')
        # Pool of workers to execture type2 requests
        workers = NestedConfig.get(self.__config,
                                   'config.workers', required=False,
                                   default=1, check=non_negative_int)
        self.__req_pool = ThreadPoolExecutor(max_workers=workers)

        # Validate config
        self.__use_mock_data = NestedConfig.get(self.__config,
                                                'config.use_mock_data',
                                                required=False, default=False)

        self.__sap_config_info = SapConfig(
            eq_hist_endp=NestedConfig.get(
                self.__config, 'config.sap.equipment_history_endpoint',
                required=True, check=non_empty_str
            ),
            eq_doc_endp=NestedConfig.get(
                self.__config, 'config.sap.equipment_document_endpoint',
                required=True, check=non_empty_str
            ),
            eq_doc_single=NestedConfig.get(
                self.__config, 'config.sap.equipment_document_single',
                required=True, check=non_empty_str
            ),
            usr=NestedConfig.get(
                self.__config, 'config.sap.usr',
                required=True, check=non_empty_str
            ),
            pwd=NestedConfig.get(
                self.__config,
                'config.sap.pwd', required=True, check=non_empty_str
            ),
            timeout=int(NestedConfig.get(
                self.__config, 'config.sap.timeout', required=False,
                default=10, check=non_negative_int
            ))
        )

    def on_startup(self):
        log.info('Startup')
        self.__data_cache.start()
        self.__integrator.start()

    def main(self):
        log.info('Running')
        loop_time = NestedConfig.get(
            self.__config, 'config.loop_time',
            required=False, default=5, check=non_negative_int
        )
        while not self.wait_for_shutdown(loop_time):
            self.__process_data()

    def on_shutdown(self, exc_info):
        log.info('Shutdown')
        self.__integrator.stop()
        self.__data_cache.stop()

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
        log.info('New T2 req for %s - %s(%r)',
                 request.asset_id, request.type_, request.data)

        if request.type_ != T2_REQUEST_SAP_DOCUMENTSINGLE:
            log.warning('Ignoring unknown request type %s',
                        request.type_)
            return
        self.__t2_do_document_req(request)

    def __integrator_respond_error(self, request):
        try:
            self.__integrator.t2_respond_error(
                request, T2ProviderFailureReason.REQ_UNHANDLED)
        except AssetUnknown:
            pass

    def __t2_do_document_req(self, request):
        decoded = json.loads(request.data.decode('utf-8'))
        try:
            instid = decoded['instid']
        except KeyError:
            log.warning('instid not in request')
            self.__integrator_respond_error(request)

        result = self.__get_document_by_instid(instid)
        if result:
            try:
                result['d']['results'][0]['String']
            except KeyError:
                log.error('Unknown file type')
                self.__integrator_respond_error(request)
                return
            try:
                value = result['d']['results'][0]['FileName']
            except KeyError:
                log.error("Error in finding mime type")
                self.__integrator_respond_error(request)
                return

            mime = guess_type(value)[0]
            if not mime:
                log.error('Unknown file type')
                self.__integrator_respond_error(request)
                return

            try:
                self.__integrator.t2_respond(
                    request, mime, a2b_base64(
                        result['d']['results'][0]['String'],
                        validate=True)
                )
            except binascii_Error:
                log.error("Failed to a2b_base64 data")
                self.__integrator_respond_error(request)
        else:
            log.error("Failed to get Document Single for: %s. %s",
                      instid, result)
            self.__integrator_respond_error(request)

    def __get_document_by_instid(self, instid):
        log.debug("Getting document by instid: %s", instid)

        if self.__use_mock_data:
            return {"d": {"results": [
                {"Instid": "123456", "FileName": "text.txt",
                 "FileType": "ASC",
                 "String": "VGltIHdhcyBoZXJlISAyMDE4LTExLTMwIDE4OjA5IQ=="}
            ]}}  # noqa

        equipment_document_single = \
            self.__sap_config_info.eq_doc_single.format(instid=instid)
        log.debug("Calling Document Single endpoint: %s",
                  equipment_document_single)
        try:
            resp = requests.get(
                equipment_document_single,
                auth=(self.__sap_config_info.usr, self.__sap_config_info.pwd),
                verify=False,
                timeout=self.__sap_config_info.timeout
            )
            log.debug("Response status: %s", resp.status_code)
        except requests.exceptions.RequestException:
            log.error("__get_document_by_instid() error")
            return None

        if resp.status_code == requests.codes['ok']:
            try:
                results = resp.json()
            except ValueError:
                log.error('Decoding JSON has failed')
                return None

        return results

    def __get_values(self, results, enable_document_hack=False, mock=False):
        """Get values from the dictionary and update it in a formatted way"""
        for item in results:
            item['Datum'] = int(search(r'\d+', item['Datum']).group())

            # If there is an equpiment number, fetch the document details
            # and append them to this item
            if enable_document_hack:
                equnr = '10000018'
                enable_document_hack = False
            elif not mock:
                try:
                    equnr = item['Equnr']
                    log.debug("Getting documents for Equnr: %s", equnr)
                except KeyError:
                    log.error("\'Equnr\' key not found for this item")
                    item['Documents'] = []
                    continue

            if mock:
                with open(MOCK_DOCUMENT_FILE, 'r') as dfp:
                    results = json.load(dfp)
            else:
                results = self.__get_document_by_equnr(equnr)

            try:
                documents = results['d']['results']
            except KeyError:
                log.error("KeyError exception in __get_data_for_asset()")
                item['Documents'] = []
                continue

            # Strip date string values and convert to epoch longs
            for document in documents:
                document['Crdat'] = int(search(
                    r'\d+', document['Crdat']).group())
                document['Chdat'] = int(search(
                    r'\d+', document['Chdat']).group())

            item['Documents'] = documents

    def __get_mock_data(self):
        log.debug("Using mock Equipment History Data data")
        with open(MOCK_DATA_FILE, 'r') as f:
            data = json.load(f)

        try:
            results = data['d']['results']
        except KeyError:
            log.error("KeyError exception in __get_data_for_asset")
            return None

        self.__get_values(results, mock=True)

        return results

    def __get_data_for_asset(self, asset_id):
        log.debug("Get Equipment History Data for: %s", asset_id)
        if self.__use_mock_data:
            return self.__get_mock_data()

        enable_document_hack = False
        if asset_id in ('1000021', '1000015'):
            enable_document_hack = True
            asset_id = 'WEBER-TEST-01'

        equipment_history_endpoint = \
            self.__sap_config_info.eq_hist_endp.format(asset_id=asset_id)
        log.debug("Calling Equipment History endpoint: %s",
                  equipment_history_endpoint)
        try:
            resp = requests.get(
                equipment_history_endpoint,
                auth=(self.__sap_config_info.usr, self.__sap_config_info.pwd),
                verify=False,
                timeout=self.__sap_config_info.timeout
            )
        except requests.exceptions.RequestException:
            log.error("RequestException in __get_data_for_asset()")
            return None

        results = None
        log.debug("Response status: %s", resp.status_code)
        if resp.status_code == requests.codes['ok']:
            data = resp.json()
            try:
                results = data['d']['results']
            except KeyError:
                log.error("KeyError exception in __get_data_for_asset()")
                return None

            self.__get_values(results, enable_document_hack=enable_document_hack)

        return results

    def __get_document_by_equnr(self, equnr):
        if not equnr:
            return None

        log.debug("Getting documents for Equnr: %s", equnr)
        equipment_document_endpoint = self.__sap_config_info.eq_doc_endp.format(equnr=equnr)
        log.debug("Calling Equipment Document endpoint: %s", equipment_document_endpoint)
        try:
            resp = requests.get(
                equipment_document_endpoint,
                auth=(self.__sap_config_info.usr, self.__sap_config_info.pwd),
                verify=False,
                timeout=self.__sap_config_info.timeout
            )
            log.debug("Response status: %s", resp.status_code)
        except requests.exceptions.RequestException:
            log.error("__get_document_by_equnr error")

        if resp.status_code == requests.codes['ok']:
            try:
                results = resp.json()
            except ValueError:
                log.error('Decoding JSON has failed')
                return None

        return results

    def __process_data(self):
        log.debug("Processing Equipment History")
        for asset_id in list(self.__assets):
            log.debug("Processing asset: %s", asset_id)
            data = self.__get_data_for_asset(asset_id)
            if data and self.__has_asset_data_changed_for(asset_id, data):
                log.debug("Publish event for %s", asset_id)
                # Publish the event based on the document type
                for item in data:
                    if not item.get('Documents'):
                        log.error("No documents found in equipment history for asset %s", asset_id)
                        continue
                    try:
                        doctype = item['Doctype']
                    except KeyError:
                        log.error("KeyError exception in __process_data")
                        continue

                    event = self.__create_document_event(asset_id, doctype, item)
                    if not event:
                        log.error("Could not create document event for this asset")
                        continue

                    log.debug("Event: %s", event)

                    try:
                        self.__integrator.publish_event(event)
                    # These will all retry
                    except EventPublishFailure as ex:
                        log.error("Event Publish Failure: %s", ex)
                    except AssetUnknown:
                        pass

                self.__cache_asset_data_for(asset_id, data)

    @classmethod
    def __create_document_event(cls, asset_id, doctype, item):
        try:
            event_time = item['Datum']
        except KeyError:
            log.error("Datum KeyError for asset_id %s", asset_id)
            return None

        try:
            event_time = datetime.datetime.utcfromtimestamp(event_time // 1000)
        except OverflowError:
            log.error("Could not create a valid datetime from %s", event_time)
            return None

        log.info("Creating document event for: %s", doctype)
        doctypes = {
            'DELI': SapEquipmentHistoryDeliverySet,
            'MAIN': SapEquipmentHistoryMaintenanceContractSet,
            'MOVE': SapEquipmentHistoryMaterialMovementSet,
            'INLO': SapEquipmentHistoryInspectionLotSet,
            'PROD': SapEquipmentHistoryProductionOrderSet,
            'INVE': SapEquipmentHistoryPhysicalInventorySet,
            'PURO': SapEquipmentHistoryPurchaseOrderSet,
            'PMOD': SapEquipmentHistoryPmOrderSet,
            'NOTI': SapEquipmentHistoryNotificationSet,
            'HIST': SapEquipmentHistoryInstallationHistorySet
        }

        try:
            return doctypes[doctype](asset_id, data=item, time=event_time)
        except KeyError:
            log.error("Unknown document type: %s", doctype)
            return None

    @classmethod
    def __compute_data_hash(cls, data):
        jdata = json.dumps(data, sort_keys=True, separators=(',', ':'))
        return hashlib_md5(jdata.encode('utf8')).hexdigest()

    # Checks to see if the given data for the asset has changed
    # since it was last processed.
    def __has_asset_data_changed_for(self, asset_id, data):

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

    # After publishing the event, update the cache
    def __cache_asset_data_for(self, asset_id, data):

        log.info("Cache asset for: %s", asset_id)
        data_hash = self.__compute_data_hash(data)
        self.__data_cache.mark_as_known(asset_id, hash=data_hash)
