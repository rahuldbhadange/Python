# Copyright (c) 2018 Rolls-Royce Power Systems AG. All rights reserved.

from concurrent.futures import ThreadPoolExecutor

import datetime
import logging
import json
from hashlib import md5 as hashlib_md5
from collections import namedtuple
import requests

from IoticAgent import ThingRunner

from ioticlabs.dt.api.integrator import (
    Integrator, IntegratorCallbacks, T2ProviderFailureReason,
    EventPublishFailure, AssetUnknown
)
from ioticlabs.dt.api.util import log_exceptions, NestedConfig

from ioticlabs.dt.common.item_cache import get_cache
from ioticlabs.dt.common.util import non_empty_str, non_negative_int


from rrps.dt.events.t2defs import T2_REQUEST_SAP_BOMASMAINT

from rrps.dt.events import SapBomAsBuiltSet

log = logging.getLogger(__name__)

MOCK_DATA_FILE = "data/mock-ibase-data.json"

SapConfig = namedtuple('SapConfig', 'bom_endp bom_endp_maint bom_usr bom_pwd bom_timeout')


class SAPBomPartSupersessionHistoryIntegrator(IntegratorCallbacks, ThingRunner):

    __TRANSFER_KEYS = frozenset((
        "ParRecno",
        "SonRecno",
        "Matnr",
        "Descr",
        "Valfr",
        "Valto"
    ))

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
        # data cache used to check that the asset has been changed or not before publishing the event
        self.__data_cache = get_cache(self.__config, config_path='integrator.asset.cache.method')

        self.__workers = NestedConfig.get(self.__config, 'config.workers', required=False, default=1,
                                          check=non_negative_int)
        self.__loop_time = NestedConfig.get(self.__config, 'config.loop_time', required=False, default=5,
                                            check=non_negative_int)

        self.__req_pool = ThreadPoolExecutor(max_workers=self.__workers)

        self.__sap_config_info = SapConfig(
            bom_endp=NestedConfig.get(
                self.__config, 'config.sap.endpoint', required=True, check=non_empty_str
            ),
            bom_endp_maint=NestedConfig.get(
                self.__config, 'config.sap.endpoint_maint', required=True, check=non_empty_str
            ),
            bom_usr=NestedConfig.get(
                self.__config, 'config.sap.usr', required=True, check=non_empty_str
            ),
            bom_pwd=NestedConfig.get(
                self.__config, 'config.sap.pwd', required=True, check=non_empty_str
            ),
            bom_timeout=int(NestedConfig.get(
                self.__config, 'config.sap.timeout', required=False, default=10, check=non_negative_int
            ))
        )

    def on_startup(self):
        log.debug('SAP Bom As Built Integrator Startup')
        self.__data_cache.start()
        self.__integrator.start()

    def main(self):
        log.debug('SAP Bom As Built Integrator Running')
        loop_time = self.__loop_time
        while not self.wait_for_shutdown(loop_time):
            self._process_sap_data()

    def on_shutdown(self, exc_info):
        log.debug('SAP Bom As Built Integrator Shutdown')
        self.__integrator.stop()
        self.__data_cache.stop()

    # for IntegratorCallbacks
    def on_asset_created(self, asset_id):
        log.debug('Asset created: %s', asset_id)
        self.__assets.add(asset_id)

    # for IntegratorCallbacks
    def on_asset_deleted(self, asset_id):
        log.debug('Asset deleted: %s', asset_id)
        self.__assets.discard(asset_id)

    # for IntegratorCallbacks
    def on_t2_request(self, request):
        self.__req_pool.submit(self.__process_t2, request)

    # Wrap since run via thread pool without handling return/exception
    @log_exceptions(log)
    def __process_t2(self, request):
        log.info('New T2 req for %s - %s(%r)', request.asset_id, request.type_, request.data)

        if request.type_ != T2_REQUEST_SAP_BOMASMAINT:
            log.warning('Ignoring unknown request type %s', request.type_)
            return
        self.__t2_do_bommaint(request)

    def __t2_do_bommaint(self, request):
        decoded = json.loads(request.data.decode('utf-8'))
        data = self._get_bom_as_maintained(request.asset_id, decoded["Valfr"])
        if data:
            to_send = self.__tidy_dict(data['d']['results'])
            self.__integrator.t2_respond(request, "application/json", json.dumps(to_send).encode('utf8'))
        else:
            self.__integrator.t2_respond_error(request, T2ProviderFailureReason.REQ_UNHANDLED)

    def __tidy_dict(self, results):
        ret = []
        for row in results:
            temp = {}
            for key in self.__TRANSFER_KEYS:
                temp[key] = row[key]
            ret.append(temp)
        return ret

    def _get_bom_as_maintained(self, asset_id, valid_from):
        log.info("Get Bom As Maintained Data for: %s %s", asset_id, valid_from)

        data = None

        # asset_id hack for RR Dev environment
        # The dev environment SAPBomAsBuiltIntegrator API uses a specific asset_id we will swap two of our test IDs.
        if asset_id in ('1000021', '1000015'):
            asset_id = '526104875'

        endpoint = self.__sap_config_info.bom_endp_maint.format(asset_id=asset_id, valid_from=valid_from)
        usr = self.__sap_config_info.bom_usr
        pwd = self.__sap_config_info.bom_pwd
        timeout = int(self.__sap_config_info.bom_timeout)

        log.debug("Calling: %s", endpoint)

        try:
            resp = requests.get(endpoint, auth=(
                usr, pwd), verify=False, timeout=timeout)
            log.debug("Response status: %s", resp.status_code)
            if resp.status_code == requests.codes['ok']:
                data = resp.json()

        except requests.exceptions.RequestException as ex:
            log.error(ex)

        return data

    def _get_data_for_asset(self, asset_id):
        log.info("Get Bom As Built Data for: %s", asset_id)

        data = None

        # asset_id hack for RR Dev environment
        # The dev environment sapbomasbuilt API uses a specific asset_id we will swap two of our test IDs.
        if asset_id in ('1000021', '1000015'):
            asset_id = '526104875'

        endpoint = self.__sap_config_info.bom_endp.format(asset_id=asset_id)
        usr = self.__sap_config_info.bom_usr
        pwd = self.__sap_config_info.bom_pwd
        timeout = int(self.__sap_config_info.bom_timeout)

        log.debug("Calling: %s", endpoint)

        try:
            resp = requests.get(endpoint, auth=(usr, pwd), verify=False, timeout=timeout)
            log.debug("Response status: %s", resp.status_code)
            if resp.status_code == requests.codes['ok']:
                data = resp.json()

        except requests.exceptions.RequestException as ex:
            log.error(ex)

        return data

    @classmethod
    def _calc_eventtime(cls, parents):
        """ create the event time with appropriate format"""
        event_time = parents[0].get('Valfr', None)
        if event_time:
            try:
                event_time = datetime.datetime.strptime(event_time, '%Y%m%d%H%M%S')
            except (OverflowError, ValueError) as ex:
                log.error("Could not create a valid datetime from %s", event_time)
                log.error(ex)
        return event_time

    def _process_sap_data(self):
        log.debug("Processing Bom As Built")
        for asset_id in list(self.__assets):
            log.debug("Processing asset: %s", asset_id)
            data = self._get_data_for_asset(asset_id)
            if data is not None and self._has_asset_data_changed_for(asset_id, data):
                log.info("Publish event for %s", asset_id)
                try:
                    items = data['d']['results']
                    parents = [i for i in items if i.get('ParRecno', None) == '']
                except KeyError as exc:
                    log.error("Data results not found: %s", exc)
                    continue

                event_time = None
                if parents:
                    event_time = self._calc_eventtime(parents)

                event = SapBomAsBuiltSet(asset_id, data=items, time=event_time)
                log.debug("Event: %s", event)
                try:
                    self.__integrator.publish_event(event)
                    self._cache_asset_data_for(asset_id, data)

                # These will all retry
                except EventPublishFailure as ex:
                    log.error("Event Publish Failure: %s", ex)
                except AssetUnknown:
                    pass

    @classmethod
    def __compute_data_hash(cls, data):
        jdata = json.dumps(data, sort_keys=True, separators=(',', ':'))
        return hashlib_md5(jdata.encode('utf8')).hexdigest()

    # Checks to see if the given data for the asset has changed
    # since it was last processed.
    def _has_asset_data_changed_for(self, asset_id, data):

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
    def _cache_asset_data_for(self, asset_id, data):

        log.info("Cache asset for: %s", asset_id)
        data_hash = self.__compute_data_hash(data)
        self.__data_cache.mark_as_known(asset_id, hash=data_hash)
