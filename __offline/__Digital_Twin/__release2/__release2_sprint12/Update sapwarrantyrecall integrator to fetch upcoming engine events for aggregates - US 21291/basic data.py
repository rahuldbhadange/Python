# Copyright (c) 2019 Rolls-Royce Power Systems AG. All rights reserved.


"""Saves basic data aka stamm aka master data for asset
"""

import logging
from datetime import datetime

import dateutil.parser
import pytz

from rrps.dt.events import SapMasterDataSet, TalendFirmwareSet
from .BaseView import BaseView

logger = logging.getLogger(__name__)


class BasicDataView(BaseView):

    def on_event(self, event):
        logger.info("%s on_event called", self.__class__.__name__)

        if isinstance(event, SapMasterDataSet):
            self._handle_sapmasterdataset(event)
        elif isinstance(event, TalendFirmwareSet):
            # add some data into the saved basic data
            self._handle_talendfirmwareset(event)

    def capture_old_data(self, event):

        try:
            return self._data_access.load(self.BASIC_DATA_TABLE, event.asset)
        except:  # pylint: disable broad-except
            logger.exception("Exception reading from table %s when capturing the old data", self.BASIC_DATA_TABLE)
            return None

    def _handle_sapmasterdataset(self, event):
        payload = event.data

        # not sure why this is coming through as a list ...
        if isinstance(event.data, list):
            payload = event.data[0]

        mapped_payload = self.map_fields(event.asset, payload)

        basic_data = self._data_access.load(self.BASIC_DATA_TABLE, event.asset)

        if not basic_data:
            basic_data = {}

        basic_data.update(mapped_payload)

        basic_data.update({"asset_id": event.asset, "source": event.source, "offset": event.offset})

        self._data_access.upsert(self.BASIC_DATA_TABLE, event.asset, basic_data)

    @staticmethod
    def map_fields(asset_id, payload):
        """ Map the fields we get back from the integrator to what the UI is expecting """
        mapped_payload = {}

        try:
            timestamp = int(payload['Datab'] / 1000)
            payload_time = datetime.fromtimestamp(timestamp)
        except Exception:
            logger.exception("problem parsing date from basic data for asset %s", asset_id)
            raise

        utc_time = pytz.utc.localize(payload_time)
        iso_format = utc_time.isoformat()

        mapped_payload['Ts'] = iso_format
        mapped_payload['Material'] = payload.get("MatnrAgg", BaseView.NO_DATA_FROM_SOURCE)
        mapped_payload['System'] = payload.get("SernrAgg", BaseView.NO_DATA_FROM_SOURCE)

        # send empty string for region and going to be removed from SAP API
        mapped_payload['Region'] = ""
        mapped_payload['MotorMaterial'] = payload.get("MatnrEng", BaseView.NO_DATA_FROM_SOURCE)
        mapped_payload['Model'] = payload.get("MaktxEng", BaseView.NO_DATA_FROM_SOURCE)
        mapped_payload['Engine'] = payload.get("SernrEng", BaseView.NO_DATA_FROM_SOURCE)

        customer = payload.get("Name1", BaseView.NO_DATA_FROM_SOURCE)
        customer_and_id = ""
        if customer:
            customer_id = payload.get("Kunde", BaseView.NO_DATA_FROM_SOURCE)
            if customer_id:
                customer_and_id = "{} ({})".format(customer, customer_id)
            else:
                customer_and_id = customer

        mapped_payload['Customer'] = customer_and_id

        # TODO: we dont know where these are coming from yet
        mapped_payload['ConnectivityDeviceNum'] = BaseView.NO_DATA_FROM_SOURCE
        mapped_payload['TrainName'] = BaseView.NO_DATA_FROM_SOURCE

        return mapped_payload

    def _handle_talendfirmwareset(self, event):
        """ set FSV to be version in existing basic data
        """
        basic_data = self._data_access.load(self.BASIC_DATA_TABLE, event.asset)

        if basic_data is None:
            logger.info("Could not load basic data for asset %s", event.asset)
            return

        utc_time = pytz.utc.localize(event.time)
        iso_format = utc_time.isoformat()
        basic_data.update({
            "Ts": iso_format,
            "FSV": event.data.get("version", BaseView.NO_DATA_FROM_SOURCE)
        })

        self._data_access.upsert(self.BASIC_DATA_TABLE, event.asset, basic_data)

    def on_field_data(self, asset_id, time, payload):
        """Update the position and operating hours of an asset basic data.
        """

        position = [-1, -1]

        if payload.get('Latitude', None) and payload.get('Longitude', None):
            position = [float(payload['Latitude']), float(payload['Longitude'])]

        utc_time = pytz.utc.localize(time)

        if 'OperatingHours' not in payload:
            return

        fd_update_time = utc_time

        basic_data = self._data_access.load(self.BASIC_DATA_TABLE, asset_id)

        if basic_data is None:
            logger.warning("Could not load basic data for asset %s", asset_id)
            return

        bd_last_update_time = None

        if basic_data.get('_last_field_data_update', None):
            bd_last_update_time = dateutil.parser.parse(basic_data['_last_field_data_update'])

        # if the field data update time is earlier than this field data update
        # then update the timestamp, position and OperatingHours
        if bd_last_update_time is not None and fd_update_time <= bd_last_update_time:
            return

        changed_data = basic_data.copy()

        operating_hours = 0
        if isinstance(payload['OperatingHours'], int):
            operating_hours = payload['OperatingHours']

        changed_data['_last_field_data_update'] = fd_update_time.isoformat()
        changed_data['OperatingHours'] = operating_hours
        changed_data['Position'] = position

        self._data_access.upsert(self.BASIC_DATA_TABLE, asset_id, changed_data)
