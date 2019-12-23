# Copyright (c) 2018 Rolls-Royce Power Systems AG. All rights reserved.

import logging
import json
import re
from hashlib import md5 as hashlib_md5
from collections import namedtuple

import requests

from IoticAgent import ThingRunner

from ioticlabs.dt.api.integrator import Integrator, IntegratorCallbacks, EventPublishFailure, AssetUnknown

from ioticlabs.dt.common.item_cache import get_cache

from ioticlabs.dt.api.util import NestedConfig
from ioticlabs.dt.common.util import non_empty_str, non_negative_int

from rrps.dt.events import SapWarrantyRecallSet

log = logging.getLogger(__name__)

#MOCK_DATA_FILE = 'data/mock-data.json'

SapConfig = namedtuple('SapConfig', 'equnr_endpoint sernr_endpoint usr pwd timeout')


class SapWarrantyRecallIntegrator(IntegratorCallbacks, ThingRunner):
    """ SapWarrantyRecallIntegrator initializing """

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
        #self.__use_mock_data = NestedConfig.get(self.__config, 'config.use_mock_data', required=False, default=False)
        self.__loop_time = NestedConfig.get(self.__config,
                                            'config.loop_time', required=False, default=5, check=non_negative_int)

        self.__sap_config_info = SapConfig(
            equnr_endpoint=NestedConfig.get(self.__config,
                                            'config.sap.equnr_endpoint', required=True, check=non_empty_str),
            sernr_endpoint=NestedConfig.get(self.__config,
                                            'config.sap.sernr_endpoint', required=True, check=non_empty_str),
            usr=NestedConfig.get(self.__config, 'config.sap.usr', required=True, check=non_empty_str),
            pwd=NestedConfig.get(self.__config, 'config.sap.pwd', required=True, check=non_empty_str),
            timeout=int(NestedConfig.get(self.__config,
                                         'config.sap.timeout', required=False, default=10, check=non_negative_int))
        )

    def on_startup(self):
        """ Starts the integrator. Other public methods herein must not be called beforehand.
        Should be called after starting Iotic agent.
        Alternatively use with keyword on the instance. """
        log.info('Sap Warranty Recall Integrator Startup')
        self.__data_cache.start()
        self.__integrator.start()

    def main(self):
        """ Sap Warranty Recall Integrator Started Running """
        log.info('Sap Warranty Recall Integrator Running')
        self.__process_data()
        loop_time = self.__loop_time
        while not self.wait_for_shutdown(loop_time):
            self.__process_data()

    def on_shutdown(self, exc_info):
        """ Stops the integrator. Should be called before shutting down the Iotic agent. """
        log.info('Sap Warranty Recall Integrator Shutdown')
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
        log.info('T2 request: %s', request)

    def __get_data_for_asset(self, asset_id):
        """ returns Sap Warranty Recall data for asset_id """
        log.info("Get Sap Warranty Recall data for: %s", asset_id)

        #data = None

        # asset_id hack for RR Dev environment
        # The dev environment SapWarrantyRecall API uses a specific asset_id we will swap two of our test IDs.
        if asset_id in ('1000021', '1000015'):
            asset_id = '5242454668'

        endpoint = self.__sap_config_info.sernr_endpoint.format(asset_id=asset_id)
        usr = self.__sap_config_info.usr
        pwd = self.__sap_config_info.pwd
        timeout = self.__sap_config_info.timeout
#        log.debug("Calling: %s", endpoint)
        log.error("Calling: %s", endpoint)

        data = self.__call_data(endpoint, usr, pwd, timeout)
        return data

    @classmethod
    def __call_data(cls, endpoint, usr, pwd, timeout):

        data = None
        try:
            resp = requests.get(endpoint, auth=(usr, pwd), verify=False, timeout=timeout)
#            log.debug("Response status: %s", resp.status_code)
            log.error("Response status: %s", resp.status_code)
            if resp.status_code == requests.codes['ok']:
                results = resp.json()
                try:
                    data = results['d']['results']
                # Strip date string values and convert to epoch longs
                    for item in data:
                        item['Refdt'] = int(re.findall(r'\d+', item['Refdt'])[0])
                except ValueError as ex:
                    log.error(ex)
            else:
                log.error("Endpoint response failed: %s", resp.status_code)

        except requests.exceptions.RequestException as ex:
            log.error(ex)

        return data

    def __process_data(self):
        """ Processing Sap Warranty Recalls data"""
        log.info("Processing Sap Warranty Recalls")
        for asset_id in list(self.__assets):
            log.debug("Processing asset: %s", asset_id)
            data = self.__get_data_for_asset(asset_id)
            if data and self.__has_asset_data_changed_for(asset_id, data):
                event = SapWarrantyRecallSet(asset_id, data=data)
                log.debug("Publishing event: %s", event)

                try:
                    self.__integrator.publish_event(event)
                    self.__cache_asset_data_for(asset_id, data)

                # These will all retry
                except EventPublishFailure as ex:
                    log.error("Event Publish Failure: %s", ex)
                except AssetUnknown:
                    pass

    @classmethod
    def __compute_data_hash(cls, data):
        """ computing data"""
        jdata = json.dumps(data, sort_keys=True, separators=(',', ':'))
        return hashlib_md5(jdata.encode('utf8')).hexdigest()

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

    # After publishing the event, update the cache
    def __cache_asset_data_for(self, asset_id, data):
        """ updating Cache asset data for asset_id """
        log.info("Cache asset for: %s", asset_id)
        data_hash = self.__compute_data_hash(data)
        self.__data_cache.mark_as_known(asset_id, hash=data_hash)
