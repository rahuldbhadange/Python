# Copyright (c) 2018 Rolls-Royce Power Systems AG. All rights reserved.

from concurrent.futures import ThreadPoolExecutor

import logging
import json
import os

import requests

from IoticAgent import ThingRunner

from ioticlabs.dt.api.integrator import Integrator, IntegratorCallbacks, T2ProviderFailureReason
from ioticlabs.dt.api.util import NestedConfig, log_exceptions

from rrps.dt.events.t2defs import T2_REQUEST_SAP_SUPERSESSION

log = logging.getLogger(__name__)


class SAPSupersessionIntegrator(IntegratorCallbacks, ThingRunner):

    def __init__(self, config, agent_config):
        super().__init__(config=agent_config)

        if not (isinstance(config, dict) and all(section in config for section in ('integrator', 'config'))):
            raise ValueError(
                'Configuration invalid / missing required section')

        # Whilst the integrator core requires particular configuration, top-level sections could be defined to provide
        # parameters specific to this integrator.
        self.__integrator = Integrator(config['integrator'], self.client, self)
        self.__config = config
        self.__data_cache = self.__config['config']['data-cache']
        self.__req_pool = ThreadPoolExecutor(max_workers=self.__config['config']['workers'])

    def on_startup(self):
        log.debug('SAP Supersession Integrator Startup')
        self.__integrator.start()

    def main(self):
        log.debug('SAP Supersession Integrator Running')
        loop_time = self.__config['config']['loop_time']
        while not self.wait_for_shutdown(loop_time):
            pass

    def on_shutdown(self, exc_info):
        log.debug('SAP Supersession Integrator Shutdown')
        self.__integrator.stop()

    # for IntegratorCallbacks
    def on_asset_created(self, asset_id):
        log.debug('Asset created: %s', asset_id)

    # for IntegratorCallbacks
    def on_asset_deleted(self, asset_id):
        log.debug('Asset deleted: %s', asset_id)

    # for IntegratorCallbacks
    def on_t2_request(self, request):
        self.__req_pool.submit(self.__process_t2, request)

    # Wrap since run via thread pool without handling return/exception
    @log_exceptions(log)
    def __process_t2(self, request):
        log.info('New T2 req for %s - %s(%r)', request.asset_id, request.type_, request.data)

        if request.type_ != T2_REQUEST_SAP_SUPERSESSION:
            log.warning('Ignoring unknown request type %s', request.type_)
            return
        self.__t2_do_sapspc(request)

    def __t2_do_sapspc(self, request):
        decoded = json.loads(request.data.decode('utf-8'))
        data = self._get_data_for_material(decoded["Matnr"])
        if data:
            self.__integrator.t2_respond(request, "application/json", json.dumps(data).encode('utf8'))
        else:
            self.__integrator.t2_respond_error(request, T2ProviderFailureReason.REQ_UNHANDLED)

    def _get_data_for_material(self, material_no):
        log.info("Get Supersession Data for: %s", material_no)

        data = None

        if self.__config['config']['use_mock_data'] == 1:
            log.debug("Using mock data")
            with open(self.MOCK_DATA_FILE, mode="r", encoding="utf-8") as f:
                results = json.load(f)

            data = results['d']['results']

            for item in data:
                item.pop("__metadata", {})  # remove the unnecessary metadata if it's there
                item['Brgew'] = self._convert_to_double(item['Brgew'])
                item['Ntgew'] = self._convert_to_double(item['Ntgew'])
                item['Laeng'] = self._convert_to_double(item['Laeng'])
                item['Breit'] = self._convert_to_double(item['Breit'])
                item['Hoehe'] = self._convert_to_double(item['Hoehe'])

        else:
            endpoint = self.__config['config']['sap']['endpoint']
            usr = self.__config['config']['sap']['usr']
            pwd = self.__config['config']['sap']['pwd']

            endpoint = endpoint.replace('XXX_MATERIAL_NO_XXX', material_no)
            timeout = int(self.__config['config']['sap']['timeout'])

            log.debug("Calling: %s", endpoint)

            try:
                resp = requests.get(endpoint, auth=(usr, pwd), verify=False, timeout=timeout)
                log.debug("Response status: %s", resp.status_code)
                if resp.status_code == requests.codes['ok']:
                    results = resp.json()

                    data = results['d']['results']

                    for item in data:
                        item.pop("__metadata", {})  # remove the unnecessary metadata if it's there
                        item['Brgew'] = self._convert_to_double(item['Brgew'])
                        item['Ntgew'] = self._convert_to_double(item['Ntgew'])
                        item['Laeng'] = self._convert_to_double(item['Laeng'])
                        item['Breit'] = self._convert_to_double(item['Breit'])
                        item['Hoehe'] = self._convert_to_double(item['Hoehe'])

            except requests.exceptions.RequestException as ex:
                log.error(ex)

        return data

    @classmethod
    def _convert_to_double(cls, str_val):
        try:
            value = float(str_val)
            return value
        except:
            log.error("Error converting str %s to float", str_val)
            return None

    MOCK_DATA_FILE = os.path.join('cfg', 'mock-data.json')
