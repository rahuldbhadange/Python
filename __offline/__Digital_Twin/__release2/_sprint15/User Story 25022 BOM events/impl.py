# Copyright (c) 2018 Rolls-Royce Power Systems AG. All rights reserved.

from concurrent.futures import ThreadPoolExecutor

import datetime
import logging
import json
from hashlib import md5 as hashlib_md5
from collections import namedtuple
import re

import requests
import pytz

from IoticAgent import RetryingThingRunner

from ioticlabs.dt.api.integrator import (
    Integrator, IntegratorCallbacks,
    T2ProviderFailureReason, AssetUnknown, ShutdownRequested, T2ResponseFailure
)
from ioticlabs.dt.api.util import log_exceptions, NestedConfig

from ioticlabs.dt.common.item_cache import get_cache
from ioticlabs.dt.common.util import non_empty_str, non_negative_int


from rrps.dt.events.t2defs import T2_REQUEST_SAP_BOMASMAINT

from rrps.dt.events import SapBomAsBuiltSet, SapBomAsIbaseChangesSet

log = logging.getLogger(__name__)

DEBUG_ENABLED = log.isEnabledFor(logging.DEBUG)

MOCK_DATA_FILE = "data/mock-ibase-data.json"

IBASE_CHANGE_DATE_FORMAT = "%Y%m%d%H%M%S"

BomConfig = namedtuple('BomConfig', 'bom_endp bom_endp_maint bom_endp_change bom_usr bom_pwd bom_timeout')


class SAPBomAsBuiltIntegrator(IntegratorCallbacks, RetryingThingRunner):

    __TRANSFER_KEYS = frozenset((
        "ParRecno",
        "SonRecno",
        "Matnr",
        "Descr",
        "Valfr",
        "Valto",
        "Sortf",
        "Sernr",
        "Yyemrel",
        "Amount",
        "Unit",
        "YYDATUM",
        "YYFKGRP",
        "YYFGRSP"
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
        self.__enable_dev_mapping = NestedConfig.get(self.__config,
                                                     'config.enable_dev_mapping', required=False, default=False)

        self.__req_pool = ThreadPoolExecutor(max_workers=self.__workers)

        self.__bom_config_info = BomConfig(
            bom_endp=NestedConfig.get(
                self.__config, 'config.bom.endpoint', required=True, check=non_empty_str
            ),
            bom_endp_maint=NestedConfig.get(
                self.__config, 'config.bom.endpoint_maint', required=True, check=non_empty_str
            ),
            bom_endp_change=NestedConfig.get(
                self.__config, 'config.bom.endpoint_change', required=True, check=non_empty_str
            ),
            bom_usr=NestedConfig.get(
                self.__config, 'config.bom.usr', required=True, check=non_empty_str
            ),
            bom_pwd=NestedConfig.get(
                self.__config, 'config.bom.pwd', required=True, check=non_empty_str
            ),
            bom_timeout=int(NestedConfig.get(
                self.__config, 'config.bom.timeout', required=False, default=10, check=non_negative_int
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
            self.__process_bom_as_built()
            self.__process_bom_changes()

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
        print("\n\n", request, "\n\n")
        self.__req_pool.submit(self.__process_t2, request)

    # Wrap since run via thread pool without handling return/exception
    @log_exceptions(log)
    def __process_t2(self, request):
        log.info('New T2 req for %s - %s(%r)', request.asset_id, request.type_, request.data)

        print("\n\n", request.asset_id, request.type_, request.data, "\n\n")

        if request.type_ != T2_REQUEST_SAP_BOMASMAINT:
            log.warning('Ignoring unknown request type %s', request.type_)
            return
        self.__t2_do_bommaint(request)

    def __tidy_dict(self, results):
        ret = []
        for row in results:
            temp = {}
            for key in self.__TRANSFER_KEYS:
                temp[key] = row[key]
                _date = row.get('YYDATUM')
                if _date:
                    temp['YYDATUM'] = int(re.findall(r'\d+', _date)[0])
            ret.append(temp)
        return sorted(ret, key=lambda i: i.get('Sortf'))

    def __integrator_t2_respond_error(self, request, reason=T2ProviderFailureReason.REQ_UNHANDLED):
        try:
            self.__integrator.t2_respond_error(request, reason)
        except ShutdownRequested:
            pass
        except TypeError:
            log.error('Could not send T2 error response, invalid request or reason', exc_info=DEBUG_ENABLED)
        except T2ResponseFailure:
            log.error('Could not send T2 error response', exc_info=DEBUG_ENABLED)

    def __integrator_t2_respond(self, request, data):
        try:
            self.__integrator.t2_respond(request, "application/json", json.dumps(data).encode('utf8'))
        except ShutdownRequested:
            pass
        except AssetUnknown:
            log.error('Could not send T2 response, asset unknown', exc_info=DEBUG_ENABLED)
        except T2ResponseFailure:
            log.error('Could not send T2 response', exc_info=DEBUG_ENABLED)

    def __t2_do_bommaint(self, request):
        asset_id = request.asset_id

        if self.__enable_dev_mapping:
            asset_id = '526104875'

        decoded = json.loads(request.data.decode('utf-8'))
        try:
            valid_from = decoded['Valfr']
            print("\n\n", valid_from, "\n\n")
        except KeyError:
            log.warning('Valfr not in request')
            self.__integrator_t2_respond_error(request)
            return

        log.info("Get Bom As Maintained Data for: %s %s", asset_id, valid_from)

        endpoint = self.__bom_config_info.bom_endp_maint.format(asset_id=asset_id, valid_from=valid_from)
        usr = self.__bom_config_info.bom_usr
        pwd = self.__bom_config_info.bom_pwd
        timeout = int(self.__bom_config_info.bom_timeout)

        log.debug("Calling: %s", endpoint)
        try:
            resp = requests.get(endpoint, auth=(usr, pwd), verify=False, timeout=timeout)
            log.debug("Response status: %s", resp.status_code)
            if resp.status_code == requests.codes.not_found:  # pylint: disable=no-member
                self.__integrator_t2_respond_error(request, reason=T2ProviderFailureReason.RESOURCE_UNKNOWN)
                return
            resp.raise_for_status()

            if resp.ok:
                try:
                    data = self.__tidy_dict(resp.json()['d']['results'])
                except:  # pyline: disable=broad-except
                    log.error("Could not parse JSON from bom as maintained response for asset %s", asset_id)
                else:
                    self.__integrator_t2_respond(request, data)
                    return

        except requests.exceptions.HTTPError as ex:
            log.error("_get_bom_as_maintained %s with asset_id: %s and valid_from: %s", ex, asset_id, valid_from)

        except requests.exceptions.RequestException as ex:
            log.error("_get_bom_as_maintained %s", ex, exc_info=DEBUG_ENABLED)

        self.__integrator_t2_respond_error(request)

    def _get_data_for_asset(self, asset_id):
        log.info("Get Bom As Built Data for: %s", asset_id)

        if self.__enable_dev_mapping:
            asset_id = '526104875'

        endpoint = self.__bom_config_info.bom_endp.format(asset_id=asset_id)
        usr = self.__bom_config_info.bom_usr
        pwd = self.__bom_config_info.bom_pwd
        timeout = int(self.__bom_config_info.bom_timeout)

        log.debug("Calling: %s", endpoint)

        try:
            resp = requests.get(endpoint, auth=(usr, pwd), verify=False, timeout=timeout)
            log.debug("Response status: %s", resp.status_code)
            resp.raise_for_status()

            if resp.ok:
                try:
                    results = resp.json()['d']['results']
                    for item in results:
                        record_date = item.get('Yydatum')
                        if record_date:
                            item['Yydatum'] = int(re.findall(r'\d+', record_date)[0])
                    return results
                except:  # pyline: disable=broad-except
                    log.error("Could not parse JSON from bom as built response for asset %s", asset_id)

        except requests.exceptions.HTTPError as ex:
            log.error("_get_data_for_asset %s with asset_id: %s", ex, asset_id)

        except requests.exceptions.RequestException as ex:
            log.error("_get_data_for_asset %s", ex, exc_info=DEBUG_ENABLED)

        return None

    def __get_bom_changes(self, asset_id, uptim=None):
        """Retrieves BOM changes for the specified asset.

        Args:
            asset_id (str): an asset identifier.
            uptim (str): the date to be passed to the API to retrieve only changes occurred after it;
                         the format of the string is %Y%m%d000000 (e.g. 20191231000000).
        """
        log.info("Getting BOM changes for asset %s", asset_id)

        if self.__enable_dev_mapping:
            asset_id = '526104875'

        # if not uptim:
        uptim = '19700101000000'

        endpoint = self.__bom_config_info.bom_endp_change.format(asset_id=asset_id, uptim=uptim)
        usr = self.__bom_config_info.bom_usr
        pwd = self.__bom_config_info.bom_pwd
        timeout = int(self.__bom_config_info.bom_timeout)

        log.debug("Calling: %s", endpoint)

        try:
            resp = requests.get(endpoint, auth=(usr, pwd), verify=False, timeout=timeout)
            log.debug("Response status: %s", resp.status_code)
            resp.raise_for_status()

            if resp.ok:
                try:
                    source_records = resp.json()['d']['results']
                    changes = []
                    for source in source_records:
                        update_time = source.get('Uptim')
                        if update_time == '0':
                            update_time = None
                        valid_from = self.timestamp(source['Valfr'])
                        valid_to = source.get('Valto')
                        if valid_to and valid_to != "99991231235959":
                            valid_to = self.timestamp(valid_to)
                        else:
                            valid_to = None
                        change = {
                            'Sernr': source['Sernr'],
                            'Crtim': self.timestamp(source['Crtim']),
                            'Uptim': (
                                update_time and
                                self.timestamp(update_time) or
                                None
                            ),
                            'InRecno': source['InRecno'],
                            'Matnr': source.get('Matnr'),
                            'Maktx': source.get('Maktx'),
                            'Valfr': valid_from,
                            'Valto': valid_to
                        }
                        changes.append(change)
                    return changes
                except:  # pyline: disable=broad-except
                    log.error("Could not parse JSON from IBase changes response for asset %s", asset_id)

        except requests.exceptions.HTTPError as ex:
            log.error("_get_data_for_asset %s with asset_id: %s", ex, asset_id)

        except requests.exceptions.RequestException as ex:
            log.error("_get_data_for_asset %s", ex, exc_info=DEBUG_ENABLED)

        return None

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

    def __process_bom_changes(self):
        log.debug("Processing Bom As IBaseChange")
        for asset_id in list(self.__assets):
            try:
                uptim = self.__data_cache.get_attr(asset_id, 'uptim')
            except KeyError:
                uptim = None

            log.debug("Processing asset: %s", asset_id)
            changes = self.__get_bom_changes(asset_id, uptim)
            if changes:
                log.info("Publish BOM change events for %s", asset_id)

                for change in changes:
                    event_time = change.get('Uptim')
                    if not event_time:
                        event_time = change.get('Crtim')
                    event_time = datetime.datetime.utcfromtimestamp(event_time)

                    event = SapBomAsIbaseChangesSet(asset_id, data=[change], time=event_time)

                    log.debug("Event: %s", event)
                    try:
                        self.__integrator.publish_event(event, retry=True)
                        uptim = (datetime.datetime.now() + datetime.timedelta(minutes=1)).strftime('%Y%m%d000000')
                        self.__data_cache.mark_as_known(asset_id, uptim=uptim)
                    except ShutdownRequested:
                        log.debug("Shutdown requested while publishing event")
                        return
                    except AssetUnknown:
                        pass

    def __process_bom_as_built(self):
        log.debug("Processing Bom As Built")
        for asset_id in list(self.__assets):
            log.debug("Processing asset: %s", asset_id)
            data = self._get_data_for_asset(asset_id)
            if data is not None and self._has_asset_data_changed_for(asset_id, data):
                log.info("Publish event for %s", asset_id)
                try:
                    items = sorted(data, key=lambda i: i.get('Sortf'))
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
                    self.__integrator.publish_event(event, retry=True)
                    self._cache_asset_data_for(asset_id, data)
                except ShutdownRequested:
                    log.debug("Shutdown requested while publishing event")
                    return
                except AssetUnknown:
                    pass

    @staticmethod
    def timestamp(timestring):
        """Converts a string with a date in the format %Y%m%d%H%M%S to a timestamp.

        Assumes that the string contains a UTC datetime.
        """
        if not timestring:
            return None
        dt = datetime.datetime.strptime(timestring, IBASE_CHANGE_DATE_FORMAT)
        return int(datetime.datetime.timestamp(pytz.utc.localize(dt)))

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
