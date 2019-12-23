# Copyright (c) 2018 Rolls-Royce Power Systems AG. All rights reserved.

import datetime
import logging
import json
import os
import re
from hashlib import md5 as hashlib_md5

import requests ### request

from IoticAgent import ThingRunner

from ioticlabs.dt.api.integrator import Integrator, IntegratorCallbacks
from ioticlabs.dt.api.integrator import EventPublishFailure
from ioticlabs.dt.api.integrator import AssetUnknown
from ioticlabs.dt.api.util import NestedConfig

from rrps.dt.events import SapMasterDataSet         ### this might be the kafka, which contains event history

log = logging.getLogger(__name__)      ### creating object for saving log


class SAPMasterDataIntegrator(IntegratorCallbacks, ThingRunner):    ####  IntegratorCallbacks is might be for feed data and action requests stoaring, ?@ where does this feed data and action requests stoaring...????

    def __init__(self, config, agent_config):   ###  where does config, agent_config came from...?????

        super().__init__(config=agent_config)           ### reinitializing class 'ThingRunner' using super(), in nested

        if not (isinstance(config, dict) and all(section in config for section in ('integrator', 'config'))):
            raise ValueError(
                'Configuration invalid / missing required section')

#??     # Whilst the integrator core requires particular configuration, top-level sections could be defined to provide   ###?? which top level section???
        # parameters specific to this integrator.
        self.__integrator = Integrator(config['integrator'], self.client, self)
        self.__assets = set()                               ### setting up asset, but where and how  ????
        self.__config = config
        self.__data_cache = self.__config['config']['data-cache']       ### this might be nested dict, 'self.__data_cache = value'

    def on_startup(self):
        log.debug('SAP Master Data Integrator Startup') ### what data and how it comes...? what is a format...???
        self.__integrator.start()

    def main(self):
        log.debug('SAP Master Data Integrator Running')  ### what data and how it comes...? what is a format...??
        loop_time = self.__config['config']['loop_time']      ### how loop_time set up...???
        while not self.wait_for_shutdown(loop_time):            ### waiting for shut down untill loop_time, might be stopping the searching of asset
            self._process_master_data()          ### calling '_process_master_data()',   @down.

    def on_shutdown(self, exc_info):         ### if commanded to shutdown then asking integrator to stop.
        log.debug('SAP Master Data Integrator Shutdown')        ### what data and how it comes...? what is a format...??
        self.__integrator.stop()             ### stop command for integrator.

    # for IntegratorCallbacks
    def on_asset_created(self, asset_id):           ### when it gets called...???
        log.debug('Asset created: %s', asset_id)
        self.__assets.add(asset_id)

    # for IntegratorCallbacks
    def on_asset_deleted(self, asset_id):           ### when it gets called...???
        log.debug('Asset deleted: %s', asset_id)
        self.__assets.discard(asset_id)

    # for IntegratorCallbacks
    def on_t2_request(self, request):               ### when it gets called...???       ### T2 request comes from app to sys
        pass

    def _get_data_for_asset(self, asset_id):                ### geting call from _process_master_data() @down.
        log.info("Get Master Data for: %s", asset_id)

        data = None

        if self.__config['config']['use_mock_data'] == 1:   ### cheacking for mock data present or not
            log.debug("Using mock master data")
            with open(self.MOCK_DATA_FILE, mode="r", encoding="utf-8") as f:
                data = json.load(f)

            # Strip junk from dates (string) and convert to epoch ints
            datab = data['d']['results'][0]['Datab']            ### might be in binary
            data['d']['results'][0]['Datab'] = int(
                re.findall(r'\d+', datab)[0])
            datbi = data['d']['results'][0]['Datbi']            ### might be in int
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

    def _process_master_data(self):             ### getting call from 'main()' @up, (waiting for shutdown - within loop_time)
        log.debug("Processing Master Data")
        for asset_id in list(self.__assets):    ## 'asset_id' came from where? # might be cheacking asset by asset_id in asset pool OR in event list i.e. kafka
            log.debug("Processing asset: %s", asset_id)
            data = self._get_data_for_asset(asset_id)               ### calling '_get_data_for_asset ()     @up
            if data is not None:      ### means might be kafka having something
                if self._has_asset_data_changed_for(asset_id, data):    #### calling it to '_has_asset_data_changed_for ()'  @down
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
                    event = SapMasterDataSet(asset_id, data=master_data, time=event_time)       ### SapMasterDataSet @(kafka) extracting event history 
                    log.debug("Event: %s", event)

                    try:
                        self.__integrator.publish_event(event)          ### publish_event(event) @integrator API
                        self._cache_asset_data_for(asset_id, data)      ### calling '_cache_asset_data_for()

                    # These will all retry
                    except EventPublishFailure as ex:
                        log.error("Event Publish Failure: %s", ex)
                    except AssetUnknown as ex:
                        pass

    # Checks to see if the given data for the asset has changed
    # since it was last processed.
##### _has_asset_data_changed_for will be same for all integrator
    def _has_asset_data_changed_for(self, asset_id, data):       ### 'data' came from _get_data_for_asset(). ### getting call from '_process_master_data()' @up
        log.info("Checking asset cache for: %s", asset_id)        ### what is 'asset cache' here, why we are checking...???
        if not os.path.exists(self.__data_cache):       ### asking whether 'asset cache', if not might be need to append. (might be in kafka(this might be an event))
            # No cache so this is new data
            return True

        filename = asset_id + '.json'       ### created file with '.json' extension
        file_path = os.path.join(self.__data_cache, filename)       ### might be putting '__data_cache' in 'filename'
###
        if not os.path.isfile(file_path):       ### checking file in the existed file path (location)
            # No file exists so this is new data
            return True

        with open(file_path, mode="r", encoding="utf-8") as f:      ### opening the newfile 
            cached_data_hash = f.read()

        data_hash = self.__compute_data_hash(data)      ### calling '__compute_data_hash(data)' @ down.
        if cached_data_hash != data_hash:           ### this might be cross cheacking for format
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

    MOCK_DATA_FILE = os.path.join('cfg', 'mock-master-data.json')                                                                            
