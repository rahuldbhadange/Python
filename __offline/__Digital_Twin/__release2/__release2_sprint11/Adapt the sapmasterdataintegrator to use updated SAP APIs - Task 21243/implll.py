# Copyright (c) 2018 Rolls-Royce Power Systems AG. All rights reserved.

import datetime
import logging
import json
import math
from hashlib import md5 as hashlib_md5

from collections import namedtuple

import requests

from IoticAgent import RetryingThingRunner

from ioticlabs.dt.api.integrator import Integrator, IntegratorCallbacks, AssetUnknown, ShutdownRequested
from ioticlabs.dt.api.util import NestedConfig

from ioticlabs.dt.common.item_cache import get_cache
from ioticlabs.dt.common.util import non_empty_str, non_negative_int

from rrps.dt.events import SapMasterDataSet

log = logging.getLogger(__name__)

DEBUG_ENABLED = log.isEnabledFor(logging.DEBUG)

SapConfig = namedtuple('SapConfig', 'hi_endp md_endp md_usr md_pwd md_timeout')


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
        self.__enable_dev_mapping = NestedConfig.get(self.__config,
                                                     'config.enable_dev_mapping', required=False, default=False,
                                                     check=non_empty_str)

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

    def __get_data_for_asset(self, asset_id):
        """ returns sapmasterdata for asset_id """
        log.info("Get Master Data for: %s", asset_id)

        # asset_id hack for RR Dev environment
        # The dev environment sapmasterdata API uses a specific asset_id we will swap two of our test IDs.
        if self.__enable_dev_mapping:
            asset_id = '1000015'

        usr = self.__sap_config_info.md_usr
        pwd = self.__sap_config_info.md_pwd
        timeout = int(self.__sap_config_info.md_timeout)

        # aggregate_equipment_number, results = self.__get_aggregate_equipment_num(asset_id, usr, pwd, timeout)
        # engine_serial = self.__get_the_engine_serial_number(asset_id, aggregate_equipment_number, results)
        engine_serial = self.__get_the_engine_serial_number(asset_id, usr, pwd, timeout)
        aggregate_data = self.__get_the_aggregate_data(asset_id, usr, pwd, timeout)
        data = self.__get_the_engine_data(engine_serial, aggregate_data, usr, pwd, timeout)

        if data:
            return data

        return None

    def __get_the_engine_serial_number(self, asset_id, usr, pwd, timeout):
        """ returns __get_the_engine_serial_number for asset_id """
        log.info("Get the Aggregate Equipment Number for asset_id: %s", asset_id)

        try:
            hi_endpoint = self.__sap_config_info.hi_endp.format(asset_id=asset_id)
            log.debug("Calling hi_endpoint: %s", hi_endpoint)

            resp = requests.get(hi_endpoint, auth=(usr, pwd), verify=False, timeout=timeout)
            log.debug("Response status: %s", resp.status_code)
            resp.raise_for_status()
            if resp.ok:
                try:
                    data = resp.json()
                    results = data['d']['results']
                    aggregate_equipment_number = None

                    for _data in results:
                        if _data['Hequi'] == "":
                            aggregate_equipment_number = _data['Equnr']
                            log.debug("Getting aggregate_equipment_number: %s",
                                      aggregate_equipment_number)
                            # return aggregate_equipment_number, results
                    for _data in results:
                        if _data["Hequi"] == aggregate_equipment_number and _data["Eqart"] == "ENG":
                            engine_serial = str(_data["Sernr"])
                            log.debug("Getting engine_serial: %s", engine_serial)
                            return engine_serial

                except:  # pylint: disable=broad-except
                    log.error("Could not parse JSON from response for asset %s",
                              asset_id, exc_info=DEBUG_ENABLED)
            else:
                log.error("Endpoint response failed: %s", resp.status_code)

        except requests.exceptions.HTTPError as ex:
            log.error("Get the Engine Serial %s with asset_id: %s", ex, asset_id)

        except requests.exceptions.RequestException as ex:
            log.error(ex, exc_info=DEBUG_ENABLED)

        return None

    # @staticmethod
    # def __get_the_engine_serial_number(asset_id, aggregate_equipment_number, results):
    #     """ returns engine_serial_number for asset_id """
    #     log.info("Get the Engine Serial Number for asset_id: %s", asset_id)
    #
    #     for _data in results:
    #         try:
    #             if _data["Hequi"] == aggregate_equipment_number and _data["Eqart"] == "ENG":
    #                 engine_serial = str(_data["Sernr"])
    #                 log.debug("Getting engine_serial: %s", engine_serial)
    #                 return engine_serial
    #         except KeyError:
    #             log.error("\'Hequi\' or \'Eqart\' key not found for this item")
    #             return None
    #
    #     return None

    def __get_the_aggregate_data(self, asset_id, usr, pwd, timeout):
        """ returns aggregate_data for asset_id """
        log.info("Get the Aggregate Data for asset_id: %s", asset_id)

        try:
            md_endpoint = self.__sap_config_info.md_endp.format(asset_id=asset_id)
            log.debug("Calling md_endpoint: %s", md_endpoint)

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
                    event_data = None
                    try:
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
                            del event_data[field]
                    except KeyError:
                        log.error("Could not find response for asset %s", asset_id)

                    return event_data
            else:
                log.error("Endpoint response failed: %s", resp.status_code)

        except requests.exceptions.HTTPError as ex:
            log.error("Get the Aggregate Data %s with asset_id: %s", ex, asset_id)

        except requests.exceptions.RequestException as ex:
            log.error(ex, exc_info=DEBUG_ENABLED)

        return None

    def __get_the_engine_data(self, engine_serial, event_data, usr, pwd, timeout):
        """ returns engine_data for engine_serial """
        log.info("Get the Engine Data for engine_serial: %s", engine_serial)

        try:
            md_endpoint = self.__sap_config_info.md_endp.format(asset_id=engine_serial)
            log.debug("Calling md_endpoint: %s", md_endpoint)

            resp = requests.get(md_endpoint, auth=(usr, pwd), verify=False, timeout=timeout)
            log.debug("Response status: %s", resp.status_code)
            resp.raise_for_status()

            if resp.ok:
                try:
                    data = resp.json()
                except:  # pylint: disable=broad-except
                    log.error("Could not parse JSON from response for asset %s",
                              engine_serial, exc_info=DEBUG_ENABLED)
                else:
                    try:
                        engine_data = data['d']['results'][0]

                        event_data['SernrEng'] = engine_data['Sernr']
                        event_data['MatnrEng'] = engine_data['Matnr']
                        event_data['MaktxEng'] = engine_data['Maktx']
                        event_data['EqunrEng'] = engine_data['Equnr']
                    except KeyError:
                        log.error("Could not find response for engine_serial %s", engine_serial)

                    return event_data
            else:
                log.error("Endpoint response failed: %s", resp.status_code)

        except requests.exceptions.HTTPError as ex:
            log.error("Get the Engine Data %s with engine_serial: %s", ex, engine_serial)

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
        """ Check whether the dat has changed or not. If its changed, create the event and publish """
        log.debug("Processing Master Data")

        for asset_id in list(self.__assets):
            log.debug("Processing asset: %s", asset_id)
            master_data = self.__get_data_for_asset(asset_id)

            if master_data and self.__has_asset_data_changed_for(asset_id, master_data):
                log.info("Publish event for %s", asset_id)

                event_time = self.__calc_eventtime(master_data)
                if master_data and event_time:
                    event = SapMasterDataSet(asset_id, data=master_data, time=event_time)
                    log.debug("Event: %s", event)
                else:
                    continue

                try:
                    self.__integrator.publish_event(event, retry=True)
                    self.__cache_assetdata_for(asset_id, master_data)
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
