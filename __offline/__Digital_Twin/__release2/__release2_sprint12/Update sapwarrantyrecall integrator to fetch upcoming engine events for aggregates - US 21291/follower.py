# Copyright (c) 2019 Rolls-Royce Power Systems AG. All rights reserved.

from pprint import pformat
import logging
import json

from IoticAgent import RetryingThingRunner
from rrps.dt.follower.rest_follower.views import (
    RiverOfNewsView, BOMAsBuiltView, BasicDataView, DocListView, UpcomingEventsView, WeatherInfoView
)
from rrps.dt.api.fielddata.follower import FdFollower, FdFollowerCallbacks
from rrps.dt.events import (
    SapBomAsBuiltSet, SapMasterDataSet, SapEquipmentHistoryMixin, TalendTimDocumentSet, TalendFirmwareSet,
    SapWarrantyRecallSet, FieldDataErrorSet, FieldDataSuccessSet, WeatherInfoSet
)

from rrps.dt.events.t2defs import (
    T2_REQUEST_SAP_MATERIAL_SUPERSESSION, T2_REQUEST_SAP_DOCUMENTSINGLE, T2_REQUEST_TALEND_DOCUMENT,
    T2_REQUEST_SAP_BOMASMAINT, T2_REQUEST_SAP_MATERIAL_MASTER_DATA
)

log = logging.getLogger(__name__)


class FollowerDataHandler(FdFollowerCallbacks, RetryingThingRunner):

    def __init__(self, config, agent_config, data_access):
        super().__init__(config=agent_config)

        if not (isinstance(config, dict) and all(section in config for section in ('follower', 'fielddata'))):
            raise ValueError(
                'Configuration invalid / missing required section')

        self.__follower = FdFollower(config['follower'], config['fielddata'], self.client, self)

        self._basic_data_view = BasicDataView(data_access)
        self._ron_view = RiverOfNewsView(data_access, self._basic_data_view)
        self._bom_view = BOMAsBuiltView(data_access)
        self._doc_list_view = DocListView(data_access)
        self._upcoming_events_view = UpcomingEventsView(data_access)
        self._weather_info_view = WeatherInfoView(data_access)

    def on_startup(self):
        log.debug('Startup')
        self.__follower.start()

    def main(self):
        log.debug('Running')
        while not self.wait_for_shutdown(60):
            pass

    def on_shutdown(self, exc_info):
        log.debug('Shutdown')
        self.__follower.stop()

    # for FollowerCallbacks
    def on_asset_created(self, asset_id):
        log.info('Asset created: %s', asset_id)

    # for FollowerCallbacks
    def on_asset_deleted(self, asset_id):
        log.info('Asset deleted: %s', asset_id)

    def on_asset_fd_available(self, asset_id):
        log.info('Field data available: %s', asset_id)

    def request_part_info(self, asset_id, material_id):
        """ make a type 2 request for part info
        """

        rqst_data = {"Matnr": material_id}

        for mime, chunk in self.__follower.t2_request(asset_id, T2_REQUEST_SAP_MATERIAL_MASTER_DATA,
                                                      data=json.dumps(rqst_data).encode('utf8'), timeout=10):
            yield mime, chunk

    def request_part_info_history(self, asset_id, material_id):
        """ make a type 2 request for part info history
        """

        rqst_data = {"Matnr": material_id}

        for mime, chunk in self.__follower.t2_request(asset_id, T2_REQUEST_SAP_MATERIAL_SUPERSESSION,
                                                      data=json.dumps(rqst_data).encode('utf8'), timeout=10):
            yield mime, chunk

    def request_bom_as_maintained(self, asset_id, at_time):
        """ make a type 2 request for the latest bom data
        """
        formatted_time = at_time.strftime("%Y%m%d%H%M%S")
        rqst_data = {"Valfr": formatted_time}

        for mime, chunk in self.__follower.t2_request(asset_id, T2_REQUEST_SAP_BOMASMAINT,
                                                      data=json.dumps(rqst_data).encode('utf8'), timeout=10):
            yield mime, chunk

    def request_sap_document(self, asset_id, instid):
        """ make a type 2 request for a sap document
        """
        rqst_data = {"instid": instid}
        for mime, chunk in self.__follower.t2_request(asset_id, T2_REQUEST_SAP_DOCUMENTSINGLE,
                                                      data=json.dumps(rqst_data).encode('utf8'), timeout=10):
            yield mime, chunk

    def request_talend_document(self, asset_id, doc_label, doc_name):
        """ make a type 2 request for a talend document
        """
        rqst_data = {"serialNumber": asset_id,
                     "documentLabel": doc_label, "documentName": doc_name}
        for mime, chunk in self.__follower.t2_request(asset_id, T2_REQUEST_TALEND_DOCUMENT,
                                                      data=json.dumps(rqst_data).encode('utf8'), timeout=10):
            yield mime, chunk

    # for FdFollowerCallbacks
    def on_event(self, event):
        log.info('Event for %s (%s)', event.asset, event.name())

        if isinstance(event, SapBomAsBuiltSet):
            self._bom_view.on_event(event)
            self._ron_view.on_event(event)
        elif isinstance(event, SapMasterDataSet):
            old_data = self._basic_data_view.capture_old_data(event)
            self._basic_data_view.on_event(event)
            self._ron_view.on_event(event, old_data)
        elif isinstance(event, TalendTimDocumentSet):
            self._doc_list_view.on_event(event)
            self._ron_view.on_event(event)
        elif isinstance(event, TalendFirmwareSet):
            old_data = self._basic_data_view.capture_old_data(event)
            self._basic_data_view.on_event(event)
            self._ron_view.on_event(event, old_data)
        elif isinstance(event, SapEquipmentHistoryMixin):
            self._doc_list_view.on_event(event)
            self._ron_view.on_event(event)
        elif isinstance(event, SapWarrantyRecallSet):
            # old_data = self._basic_data_view.capture_old_data(event)
            old_data = self._upcoming_events_view.capture_old_data(event)
            self._upcoming_events_view.on_event(event, old_data)
            # self._upcoming_events_view.on_event(event)
            self._doc_list_view.on_event(event)
            self._ron_view.on_event(event)
        elif isinstance(event, FieldDataErrorSet):
            # TODO: this was commented on customer request at the end of MVP1
            # self._ron_view.on_event(event)
            pass
        elif isinstance(event, FieldDataSuccessSet):
            pass
        elif isinstance(event, WeatherInfoSet):
            self._weather_info_view.on_event(event)
        else:
            log.info('Unhandled event for %s (%s)', event.asset, event.name())
            return

        self.__follower.ack_event(event)

    # field data
    def on_fielddata(self, sample):
        log.info('Field data')

        val_dict = {}

        for value in sample.template.values:
            val_dict[value.label] = value.value

        # NOTE: skip writing field data to Cosmos as it is not displayed anywhere
        self._basic_data_view.on_field_data(sample.asset, sample.time, val_dict)

    def on_event_unmatched(self, event):
        log.info(
            '[%s] #%d %s (from %s) @ %s\n%s', event.asset, event.offset, event.name(
            ), event.source, event.time,
            pformat(event.data)
        )
        # Indicate that event has been processed. If asset has been deleted in the mean time, this will be a no-op.
        self.__follower.ack_event(event)

    def on_event_internal(self, event):
        log.info('Internal: %s', event)
