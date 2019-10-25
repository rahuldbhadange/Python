# Copyright (c) 2018 Rolls-Royce Power Systems AG. All rights reserved.

import datetime
import logging
import json
import math
import re
from hashlib import md5 as hashlib_md5

from collections import namedtuple
import requests


from IoticAgent import RetryingThingRunner

from ioticlabs.dt.api.integrator import Integrator, IntegratorCallbacks, AssetUnknown, ShutdownRequested
from ioticlabs.dt.api.util import NestedConfig

from ioticlabs.dt.common.item_cache import get_cache
from ioticlabs.dt.common.util import non_empty_str, non_negative_int
from requests import delete

from rrps.dt.events import SapMasterDataSet

log = logging.getLogger(__name__)

DEBUG_ENABLED = log.isEnabledFor(logging.DEBUG)

SapConfig = namedtuple('SapConfig', 'hi_endp md_endp md_usr md_pwd md_timeout')

MOCK_DATA_FILE = "data/mock-master-data.json"


class SAPMasterDataIntegrator(IntegratorCallbacks, RetryingThingRunner):

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

        self.__loop_time = NestedConfig.get(self.__config, 'config.loop_time', required=False, default=False)

        self.__sap_config_info = SapConfig(
            hi_endp=NestedConfig.get(
                self.__config, 'config.sap.hierarchy_endpoint', required=True, check=non_empty_str
            ),
            md_endp=NestedConfig.get(
                self.__config, 'config.sap.master_endpoint', required=True, check=non_empty_str
            ),
            md_usr=NestedConfig.get(
                self.__config, 'config.sap.usr', required=True, check=non_empty_str
            ),
            md_pwd=NestedConfig.get(
                self.__config, 'config.sap.pwd', required=True, check=non_empty_str
            ),
            md_timeout=int(NestedConfig.get(
                self.__config, 'config.sap.timeout', required=False, default=10, check=non_negative_int
            ))
        )

    def on_startup(self):
        log.debug('SAP Master Data Integrator Startup')
        self.__data_cache.start()
        self.__integrator.start()

    def main(self):
        log.debug('SAP Master Data Integrator Running')
        loop_time = self.__loop_time
        while not self.wait_for_shutdown(loop_time):
            self.__process_master_data()

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

    def _response(self, asset_id, usr, pwd, timeout, hi_endpoint):

        try:
            resp = requests.get(hi_endpoint, auth=(
                usr, pwd), verify=False, timeout=timeout)
            log.debug("Response status: %s", resp.status_code)
            resp.raise_for_status()

            try:
                data = resp.json()
            except:  # pylint: disable=broad-except
                log.error("Could not parse JSON from response for asset %s", asset_id, exc_info=DEBUG_ENABLED)
            else:
                try:
                    if data['d']['results'][0]['Hequi'] == "":
                        aggregate_equipment_number = data['d']['results'][0]['Equnr']
                        try:
                            if data['d']['results'][0]['Hequi'] == aggregate_equipment_number and data['d']['results'][
                                'Eqart'] == "ENG":
                                engine_serial = data['d']['results'][0]['Sernr']
                                md_endpoint = self.__sap_config_info.md_endp.format(serial_number_of_the_aggregate=asset_id)
                                try:
                                    resp = requests.get(md_endpoint, auth=(usr, pwd), verify=False, timeout=timeout)
                                    log.debug("Response status: %s", resp.status_code)
                                    resp.raise_for_status()
                                    if resp.ok:
                                        try:
                                            data = resp.json()
                                        except:  # pylint: disable=broad-except
                                            log.error("Could not parse JSON from response for asset %s",
                                                      asset_id, exc_info=DEBUG_ENABLED)
                                        else:
                                            event_data = data['d']['results'][0]
                                            event_data['Datab'] = math.floor(
                                                datetime.datetime.strptime(event_data['Datab'],
                                                                           '%Y-%m-%d').timestamp()) * 1000
                                            event_data['Datbi'] = math.floor(
                                                datetime.datetime.strptime(event_data['Datbi'],
                                                                           '%Y-%m-%d').timestamp()) * 1000
                                            event_data['EqunrAgg'] = event_data['Equnr']
                                            event_data['MaktxAgg'] = event_data['Maktx']
                                            event_data['MatnrAgg'] = event_data['Matnr']
                                            event_data['SernrAgg'] = event_data['Sernr']
                                            for field in ('Equnr', 'Maktx', 'Matnr', 'Sernr'):
                                                delete
                                                event_data[field]

                                            md_endpoint = self.__sap_config_info.md_endp.format(
                                                serial_number_of_the_aggregate=engine_serial)
                                            try:
                                                resp = requests.get(md_endpoint, auth=(usr, pwd), verify=False,
                                                                    timeout=timeout)
                                                log.debug("Response status: %s", resp.status_code)
                                                resp.raise_for_status()
                                                if resp.ok:
                                                    try:
                                                        data = resp.json()
                                                    except:  # pylint: disable=broad-except
                                                        log.error(
                                                            "Could not parse JSON from response for asset %s",
                                                            engine_serial, exc_info=DEBUG_ENABLED)
                                                    else:
                                                        engine_data = resp.json()['d']['results'][0]
                                                        event_data['SernrEng'] = engine_data['Sernr']
                                                        event_data['MatnrEng'] = engine_data['Matnr']
                                                        event_data['MaktxEng'] = engine_data['Maktx']
                                                        event_data['EqunrEng'] = engine_data['Equnr']

                                                        return event_data
                                            except:  # pylint: disable=broad-except
                                                log.error("Could not parse object from response for asset %s", asset_id,
                                                          exc_info=DEBUG_ENABLED)

                        except requests.exceptions.HTTPError as ex:
                            log.error("%s with asset_id: %s", ex, asset_id)
                except requests.exceptions.RequestException as ex:
                    log.error(ex, exc_info=DEBUG_ENABLED)
        except requests.exceptions.RequestException as ex:
            log.error(ex, exc_info=DEBUG_ENABLED)

    def __get_data_for_asset(self, asset_id):
        log.info("Get Master Data for: %s", asset_id)

        # asset_id hack for RR Dev environment
        # The dev environment sapmasterdata API uses a specific asset_id we will swap two of our test IDs.
        # if asset_id in ('1000021', '1000015'):
        #     log.warning("Swapping asset_id %s for test id 4711-001", asset_id)
        #     asset_id = '4711-001'

        # md_endpoint = self.__sap_config_info.md_endp.format(serial_number_of_the_aggregate=asset_id)
        # hi_endpoint = self.__sap_config_info.md_endp.format(serial_number_of_the_aggregate=asset_id)
        usr = self.__sap_config_info.md_usr
        pwd = self.__sap_config_info.md_pwd
        timeout = int(self.__sap_config_info.md_timeout)

        if asset_id == "4711-0006":
            hi_endpoint = self.__sap_config_info.hi_endp.format(serial_number_of_the_aggregate=asset_id)
            log.debug("Calling: %s", hi_endpoint)
            data = self._response(asset_id, usr, pwd, timeout, hi_endpoint)
            if data:
                return data

            return None

        elif asset_id == "150001":
            hi_endpoint = self.__sap_config_info.hi_endp.format(serial_number_of_the_aggregate=asset_id)
            log.debug("Calling: %s", hi_endpoint)
            data = self._response(asset_id, usr, pwd, timeout, hi_endpoint)
            if data:
                return data

            return None

        else:   # asset_id == "150001":

            hi_endpoint = self.__sap_config_info.hi_endp.format(serial_number_of_the_aggregate=asset_id)
            log.debug("Calling: %s", hi_endpoint)

            try:
                resp = requests.get(hi_endpoint, auth=(
                    usr, pwd), verify=False, timeout=timeout)
                log.debug("Response status: %s", resp.status_code)
                resp.raise_for_status()

                if resp.ok:
                    try:
                        data = resp.json()
                    except:  # pylint: disable=broad-except
                        log.error("Could not parse JSON from response for asset %s", asset_id, exc_info=DEBUG_ENABLED)
                    else:
                        try:
                            datab = data['d']['results'][0]['Datab']
                            # Strip junk from dates (string) and convert to ints
                            data['d']['results'][0]['Datab'] = int(re.findall(r'\d+', datab)[0])
                            datbi = data['d']['results'][0]['Datbi']
                            data['d']['results'][0]['Datbi'] = int(re.findall(r'\d+', datbi)[0])
                            return data
                        except:  # pylint: disable=broad-except
                            log.error("Could not parse object from response for asset %s", asset_id, exc_info=DEBUG_ENABLED)

            except requests.exceptions.HTTPError as ex:
                log.error("%s with asset_id: %s", ex, asset_id)
            except requests.exceptions.RequestException as ex:
                log.error(ex, exc_info=DEBUG_ENABLED)

            return None

    @classmethod
    def __calc_eventtime(cls, master_data):
        """ calculate the event time with appropriate format """
        event_time = master_data.get('Datab', None)
        if event_time:
            try:
                event_time = datetime.datetime.utcfromtimestamp(event_time // 1000)
            except (OverflowError, ValueError) as exc:
                log.error("Could not create a valid datetime from %s", event_time)
                log.error(exc)
        return event_time

    def __process_master_data(self):
        """ Check whether the data has changed or not. If its changed, create the event and publish """
        log.debug("Processing Master Data")
        for asset_id in list(self.__assets):
            log.debug("Processing asset: %s", asset_id)
            data = self.__get_data_for_asset(asset_id)
            if data and self.__has_asset_data_changed_for(asset_id, data):
                log.info("Publish event for %s", asset_id)
                try:
                    master_data = data['d']['results'][0]
                except KeyError:
                    log.error("Data has not received as per spec")
                    continue

                event_time = self.__calc_eventtime(master_data)
                if master_data and event_time:
                    event = SapMasterDataSet(asset_id, data=master_data, time=event_time)
                    log.debug("Event: %s", event)
                else:
                    continue

                try:
                    self.__integrator.publish_event(event, retry=True)
                    self.__cache_assetdata_for(asset_id, data)
                except ShutdownRequested:
                    log.debug("Shutdown requested while publishing event")
                    return
                except AssetUnknown:
                    pass

    @classmethod
    def __compute_data_hash(cls, data):
        """ compute the md5 hash for the particular data"""
        jdata = json.dumps(data, sort_keys=True, separators=(',', ':'))
        return hashlib_md5(jdata.encode('utf8')).hexdigest()

    # Checks to see if the given data for the asset has changed
    # since it was last processed.
    def __has_asset_data_changed_for(self, asset_id, data):
        """ checking whether asset data has changed or not """
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
    def __cache_assetdata_for(self, asset_id, data):
        """ update the cache for the asset id """
        log.info("Cache asset for: %s", asset_id)
        data_hash = self.__compute_data_hash(data)
        self.__data_cache.mark_as_known(asset_id, hash=data_hash)
