# Copyright (c) 2018 Rolls-Royce Power Systems AG. All rights reserved.

import datetime
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

from ioticlabs.dt.common.item_cache import get_cache

from rrps.dt.events import SapMasterDataSet

log = logging.getLogger(__name__)


class SAPMasterDataIntegrator(IntegratorCallbacks, ThingRunner):

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
        self.__data_cache = get_cache(config, config_path='integrator.asset.cache.method')

    def on_startup(self):
        log.debug('SAP Master Data Integrator Startup')
        self.__data_cache.start()
        self.__integrator.start()

    def main(self):
        log.debug('SAP Master Data Integrator Running')
        loop_time = self.__config['config']['loop_time']
        while not self.wait_for_shutdown(loop_time):
            self._process_master_data()

    def on_shutdown(self, exc_info):
        log.debug('SAP Master Data Integrator Shutdown')
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
        pass

    MOCK_DATA_FILE = os.path.join('cfg', 'mock-master-data.json')

    def _get_data_for_asset(self, asset_id):
        log.info("Get Master Data for: %s", asset_id)

        data = None

        if self.__config['config']['use_mock_data'] == 1:
            log.debug("Using mock master data")
            with open(self.MOCK_DATA_FILE, mode="r", encoding="utf-8") as f:
                data = json.load(f)

            # Strip junk from dates (string) and convert to epoch ints
            datab = data['d']['results'][0]['Datab']
            data['d']['results'][0]['Datab'] = int(
                re.findall(r'\d+', datab)[0])
            datbi = data['d']['results'][0]['Datbi']
            data['d']['results'][0]['Datbi'] = int(
                re.findall(r'\d+', datbi)[0])

        else:
            endpoint = self.__config['config']['bomgar']['endpoint']
            usr = self.__config['config']['bomgar']['usr']
            pwd = self.__config['config']['bomgar']['pwd']

            key = 'config.enable_sap_sample_serial_hack'
            if NestedConfig.get(self.__config, key, required=False, default=False, check=bool):
                if asset_id == '1000021' or asset_id == '1000015':
                    asset_id = '4711-001'

            endpoint = endpoint.replace('XXX_ASSET_ID_XXX', asset_id)
            timeout = int(self.__config['config']['bomgar']['timeout'])

            log.debug("Calling: %s", endpoint)

            try:
                resp = requests.get(endpoint, auth=(
                    usr, pwd), verify=False, timeout=timeout)
                log.debug("Response status: %s", resp.status_code)
                if resp.status_code == requests.codes['ok']:
                    data = resp.json()
                    if len(data['d']['results']) == 0:
                        return data
                    # Strip junk from dates (string) and convert to ints
                    datab = data['d']['results'][0]['Datab']
                    data['d']['results'][0]['Datab'] = int(
                        re.findall(r'\d+', datab)[0])
                    datbi = data['d']['results'][0]['Datbi']
                    data['d']['results'][0]['Datbi'] = int(
                        re.findall(r'\d+', datbi)[0])

            except requests.exceptions.RequestException as ex:
                log.error(ex)

        return data

    def _process_master_data(self):
        log.debug("Processing Master Data")
        for asset_id in list(self.__assets):
            log.debug("Processing asset: %s", asset_id)
            data = self._get_data_for_asset(asset_id)
            if data is not None:
                if self._has_asset_data_changed_for(asset_id, data):
                    log.info("Publish event for %s", asset_id)
                    if len(data['d']['results']) == 0:
                        continue

                    master_data = data['d']['results'][0]
                    event_time = master_data.get('Datab', None)
                    if event_time is not None:
                        try:
                            event_time = datetime.datetime.utcfromtimestamp(event_time // 1000)
                        except Exception as ex:
                            log.error("Could not create a valid datetime from %s", event_time)
                            log.error(ex)
                    event = SapMasterDataSet(asset_id, data=master_data, time=event_time)
                    log.debug("Event: %s", event)

                    try:
                        self.__integrator.publish_event(event)
                        self._cache_asset_data_for(asset_id, data)

                    # These will all retry
                    except EventPublishFailure as ex:
                        log.error("Event Publish Failure: %s", ex)
                    except AssetUnknown as ex:
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