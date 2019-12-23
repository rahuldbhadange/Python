# Copyright (c) 2018 Rolls-Royce Power Systems AG. All rights reserved.

from concurrent.futures import ThreadPoolExecutor

import datetime
import logging
import json
import os
from hashlib import md5 as hashlib_md5

import requests

from IoticAgent import ThingRunner

from ioticlabs.dt.api.integrator import Integrator, IntegratorCallbacks, T2ProviderFailureReason
from ioticlabs.dt.api.integrator import EventPublishFailure
from ioticlabs.dt.api.integrator import AssetUnknown
from ioticlabs.dt.api.util import log_exceptions
from ioticlabs.dt.api.util import NestedConfig

from rrps.dt.events.t2defs import T2_REQUEST_SAP_BOMASMAINT

from rrps.dt.events import SapBomAsBuiltSet

log = logging.getLogger(__name__)


class SAPBomAsBuiltIntegrator(IntegratorCallbacks, ThingRunner):

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
        self.__data_cache = self.__config['config']['data-cache']
        self.__req_pool = ThreadPoolExecutor(max_workers=self.__config['config']['workers'])

    def on_startup(self):
        log.debug('SAP Bom As Built Integrator Startup')
        self.__integrator.start()

    def main(self):
        log.debug('SAP Bom As Built Integrator Running')
        loop_time = self.__config['config']['loop_time']
        while not self.wait_for_shutdown(loop_time):
            self._process_sap_data()

    def on_shutdown(self, exc_info):
        log.debug('SAP Bom As Built Integrator Shutdown')
        self.__integrator.stop()

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

        if self.__config['config']['use_mock_data'] == 1:
            log.debug("Using mock bom data")
            with open(self.MOCK_DATA_FILE, mode="r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            endpoint = self.__config['config']['bomgar']['endpoint_maint']
            usr = self.__config['config']['bomgar']['usr']
            pwd = self.__config['config']['bomgar']['pwd']

            key = 'config.enable_sap_sample_serial_hack'
            if NestedConfig.get(self.__config, key, required=False, default=False, check=bool):
                if asset_id == '1000021' or asset_id == '1000015':
                    asset_id = '526104875'

            endpoint = endpoint.replace('XXX_ASSET_ID_XXX', asset_id)
            endpoint = endpoint.replace('XXX_VALID_FROM_XXX', valid_from)
            timeout = int(self.__config['config']['bomgar']['timeout'])

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

        if self.__config['config']['use_mock_data'] == 1:
            log.debug("Using mock bom data")
            with open(self.MOCK_DATA_FILE, mode="r", encoding="utf-8") as f:
                data = json.load(f)

        else:
            endpoint = self.__config['config']['bomgar']['endpoint']
            usr = self.__config['config']['bomgar']['usr']
            pwd = self.__config['config']['bomgar']['pwd']

            key = 'config.enable_sap_sample_serial_hack'
            if NestedConfig.get(self.__config, key, required=False, default=False, check=bool):
                if asset_id == '1000021' or asset_id == '1000015':
                    asset_id = '526104875'

            endpoint = endpoint.replace('XXX_ASSET_ID_XXX', asset_id)
            timeout = int(self.__config['config']['bomgar']['timeout'])

            log.debug("Calling: %s", endpoint)

            try:
                resp = requests.get(endpoint, auth=(usr, pwd), verify=False, timeout=timeout)
                log.debug("Response status: %s", resp.status_code)
                if resp.status_code == requests.codes['ok']:
                    data = resp.json()

            except requests.exceptions.RequestException as ex:
                log.error(ex)

        return data

    def _process_sap_data(self):
        log.debug("Processing Bom As Built")
        for asset_id in list(self.__assets):
            log.debug("Processing asset: %s", asset_id)
            data = self._get_data_for_asset(asset_id)
            if data is not None:
                if self._has_asset_data_changed_for(asset_id, data):
                    log.info("Publish event for %s", asset_id)

                    items = data['d']['results']
                    parents = [i for i in items if i.get('ParRecno', None) == '']
                    event_time = None
                    if parents:
                        event_time = parents[0].get('Valfr', None)
                    if event_time:
                        try:
                            event_time = datetime.datetime.strptime(event_time, '%Y%m%d%H%M%S')
                        except Exception as ex:
                            log.error("Could not create a valid datetime from %s", event_time)
                            log.error(ex)

                    event = SapBomAsBuiltSet(asset_id, data=data['d']['results'], time=event_time)
                    log.debug("Event: %s", event)
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

    MOCK_DATA_FILE = os.path.join('cfg', 'mock-ibase-data.json')
