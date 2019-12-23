# Copyright (c) 2018 Rolls-Royce Power Systems AG. All rights reserved.

import logging
import json
import os
import re
from hashlib import md5 as hashlib_md5

import requests

from IoticAgent import ThingRunner

from ioticlabs.dt.api.integrator import Integrator, IntegratorCallbacks
from ioticlabs.dt.api.integrator import EventPublishFailure
from ioticlabs.dt.api.integrator import AssetUnknown

from ioticlabs.dt.api.util import NestedConfig

from rrps.dt.events import SapWarrantyRecallSet

log = logging.getLogger(__name__)


class SapWarrantyRecallIntegrator(IntegratorCallbacks, ThingRunner):

    def __init__(self, config, agent_config):

        super().__init__(config=agent_config)

        if not (isinstance(config, dict) and all(section in config for section in ('integrator', 'config'))):
            raise ValueError('Configuration invalid / missing required section')

        # Whilst the integrator core requires particular configuration, top-level sections could be defined to provide
        # parameters specific to this integrator.
        self.__integrator = Integrator(config['integrator'], self.client, self)
        self.__assets = set()
        self.__config = config
        self.__data_cache = self.__config['config']['data-cache']

    def on_startup(self):
        log.info('Sap Warranty Recall Integrator Startup')

        self.__integrator.start()

    def main(self):
        log.info('Sap Warranty Recall Integrator Running')
        self._process_data()
        loop_time = self.__config['config']['loop_time']
        while not self.wait_for_shutdown(loop_time):
            self._process_data()

    def on_shutdown(self, exc_info):
        log.info('Sap Warranty Recall Integrator Shutdown')
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
        pass

    def _get_data_for_asset(self, asset_id):
        log.info("Get Sap Warranty Recall data for: %s", asset_id)

        data = None

        if self.__config['config']['use_mock_data'] == 1:
            log.debug("Using mock data")
            with open(self.MOCK_DATA_FILE, mode="r", encoding="utf-8") as f:
                results = json.load(f)

            data = results['d']['results']
            # Strip date string values and convert to epoch longs
            for item in data:
                item['Refdt'] = int(re.findall(r'\d+', item['Refdt'])[0])

        else:
            endpoint = self.__config['config']['sap']['sernr_endpoint']

            key = 'config.enable_sap_sample_serial_hack'
            if NestedConfig.get(self.__config, key, required=False, default=False, check=bool):
                if asset_id == '1000021' or asset_id == '1000015':
                    asset_id = '5242454668'

            endpoint = endpoint.replace('XXX_ASSET_ID_XXX', asset_id)
            usr = self.__config['config']['sap']['usr']
            pwd = self.__config['config']['sap']['pwd']
            timeout = int(self.__config['config']['sap']['timeout'])

            log.debug("Calling: %s", endpoint)

            try:
                resp = requests.get(endpoint, auth=(usr, pwd), verify=False, timeout=timeout)
                log.debug("Response status: %s", resp.status_code)
                if resp.status_code == requests.codes['ok']:
                    results = resp.json()

                    data = results['d']['results']
                    # Strip date string values and convert to epoch longs
                    for item in data:
                        item['Refdt'] = int(re.findall(r'\d+', item['Refdt'])[0])

                else:
                    log.error("Endpoint response failed: %s", resp.status_code)

            except requests.exceptions.RequestException as ex:
                log.error(ex)

        return data

    def _process_data(self):
        log.info("Processing Sap Warranty Recalls")
        for asset_id in list(self.__assets):
            log.debug("Processing asset: %s", asset_id)
            data = self._get_data_for_asset(asset_id)
            if data is not None:
                if self._has_asset_data_changed_for(asset_id, data):

                    event = SapWarrantyRecallSet(asset_id, data=data)

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

