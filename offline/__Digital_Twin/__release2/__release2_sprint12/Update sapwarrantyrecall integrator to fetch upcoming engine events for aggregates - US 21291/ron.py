# Copyright (c) 2019 Rolls-Royce Power Systems AG. All rights reserved.

"""Saves River of News updates
"""

import logging
import urllib.parse
import pytz

from rrps.dt.events import (
    SapMasterDataSet, SapBomAsBuiltSet, SapEquipmentHistoryMixin, TalendTimDocumentSet, TalendFirmwareSet,
    SapWarrantyRecallSet, FieldDataErrorSet
)
from .BaseView import BaseView

logger = logging.getLogger(__name__)


MASTER_DATA_FIELDS_WITH_HISTORY = ["Material", "System", "Region", "MotorMaterial", "Model", "Engine", "Customer",
                                   "ConnectivityDeviceNum", "TrainName"]


class RiverOfNewsView(BaseView):

    def __init__(self, data_access, basic_data_view):
        super().__init__(data_access)
        self.__basic_data_view = basic_data_view

    def on_event(self, event, old_data=None):
        logger.info("%s on_event called", self.__class__.__name__)

        payload = event.data

        if isinstance(event, SapWarrantyRecallSet):
            for item in payload:
                # check that this item has been closed before adding to the river of news
                if isinstance(event, SapWarrantyRecallSet) and not self._is_kif_item_closed(item):
                    continue

                self._handle_item(event, item)
        else:
            self._handle_item(event, payload, old_data)

    def _handle_item(self, event, item, old_data=None):

        if isinstance(event, SapMasterDataSet):
            new_data = self.__basic_data_view.map_fields(event.asset, event.data)
            changes = self.__compare_two_dicts(MASTER_DATA_FIELDS_WITH_HISTORY, new_data, old=old_data)

            for change in changes:
                data_to_save = {}

                utc_time = pytz.utc.localize(event.time)
                iso_format = utc_time.isoformat()

                data_to_save['asset_id'] = event.asset
                data_to_save['Source'] = event.source
                data_to_save['Ts'] = iso_format
                data_to_save['Seq'] = event.offset
                data_to_save['Type'] = event.name()
                data_to_save['Details'] = []
                data_to_save['ValidFrom'] = new_data["Ts"]
                data_to_save['Attachments'] = []
                data_to_save['Description'] = "Master Data Change"
                data_to_save['FieldName'] = change['FieldName']
                data_to_save['FieldOldValue'] = change['FieldOldValue']
                data_to_save['FieldNewValue'] = change['FieldNewValue']

                self._data_access.save(self.RON_DATA_TABLE, event.asset, data_to_save)

        elif isinstance(event, SapBomAsBuiltSet):

            data_to_save = {}

            utc_time = pytz.utc.localize(event.time)
            iso_format = utc_time.isoformat()

            data_to_save['asset_id'] = event.asset
            data_to_save['Source'] = event.source
            data_to_save['Ts'] = iso_format
            data_to_save['Seq'] = event.offset
            data_to_save['Type'] = event.name()
            data_to_save['Description'] = "BoM as built set"
            data_to_save['Attachments'] = []

            creation_date = event.time.strftime("%d.%m.%Y")
            data_to_save['Details'] = [{"Type": "IBASE as Built",
                                        "CreationDate": creation_date}]

            self._data_access.save(self.RON_DATA_TABLE, event.asset, data_to_save)

        elif isinstance(event, TalendFirmwareSet):
            new_value = event.data.get('version')

            if old_data:
                old_value = old_data.get('FSV')
            else:
                old_value = None

            if new_value != old_value:
                utc_time = pytz.utc.localize(event.time)
                iso_format = utc_time.isoformat()
                formatted_date = event.time.strftime("%d.%m.%Y")

                entry = {
                    'asset_id': event.asset,
                    'Description': 'FSW Version',
                    'FieldName': 'FSV',
                    'FieldOldValue': old_value,
                    'FieldNewValue': new_value,
                    'Source': event.source,
                    'Ts': iso_format,
                    'FormattedDate': formatted_date,
                    'Seq': event.offset,
                    'Type': event.name(),
                    'Details': [],
                    'Attachments': []
                }
                self._data_access.save(self.RON_DATA_TABLE, event.asset, entry)
        else:
            self.__default_handle_item(event, item)

    def __default_handle_item(self, event, item):

        data_to_save = {}

        utc_time = pytz.utc.localize(event.time)
        iso_format = utc_time.isoformat()

        data_to_save['asset_id'] = event.asset
        data_to_save['Source'] = event.source
        data_to_save['Ts'] = iso_format
        data_to_save['Seq'] = event.offset

        event_specific = self._get_event_specific(event, item)

        data_to_save.update(event_specific)
        self._data_access.save(self.RON_DATA_TABLE, event.asset, data_to_save)

    @staticmethod
    def _create_sap_attachments_list(asset_id, doc_list):
        """ create a list of doc names and links to the documents """
        name_link_list = []

        for doc in doc_list:
            doc_name = doc.get("Docnam", BaseView.NO_DATA_FROM_SOURCE)
            instid = doc.get("Instid", BaseView.NO_DATA_FROM_SOURCE)

            if doc_name and instid:
                name_link = {"Name": doc_name,
                             "Link": "document/{}/{}.{}".format(asset_id, urllib.parse.quote(instid),
                                                                urllib.parse.quote(doc.get("FileExt")))}
                name_link_list.append(name_link)
            else:
                logger.warning(
                    "Docnam or Instid is empty so not adding to list of attachments")
                logger.warning(doc)

        return name_link_list

    @staticmethod
    def _create_talend_attachments_list(asset_id, doc_list):
        """ create a list of doc names and links to the documents """
        name_link_list = []

        for doc in doc_list:
            doc_name = doc.get("documentName", BaseView.NO_DATA_FROM_SOURCE)
            doc_label = doc.get("documentLabel", BaseView.NO_DATA_FROM_SOURCE)

            if doc_name:
                name_link = {"Name": doc_name,
                             "Link": "talend-doc/{}/{}/{}".format(asset_id, urllib.parse.quote(doc_label),
                                                                  urllib.parse.quote(doc_name))}
                name_link_list.append(name_link)

        return name_link_list

    @staticmethod
    def extract_field_data_error(errors_list):
        if not isinstance(errors_list, list):
            raise ValueError("Expecting field data error to be a list")

        if not errors_list:
            return "No blob name", "No error message"

        msg = ""
        for error in errors_list:
            msg = msg + " " + error.get("Error")

        blob_name = errors_list[0].get("Blobname")

        return blob_name, msg

    @classmethod
    def __compare_two_dicts(cls, fields, new, old=None):
        changes = []
        for field in fields:
            new_value = new.get(field)
            if old:
                old_value = old.get(field)
            else:
                old_value = None
            if old_value != new_value:
                changes.append({'FieldName': field, 'FieldOldValue': old_value, 'FieldNewValue': new_value})

        return changes

    def _get_event_specific(self, event, item):
        event_specific = {}

        event_specific['Type'] = event.name()
        event_specific['Description'] = type(event)
        event_specific['Details'] = []
        event_specific['Attachments'] = []

        if isinstance(event, SapMasterDataSet):
            event_specific['Type'] = event.name()
            event_specific['Description'] = "Master Data Change"
            event_specific['Details'] = []
        elif isinstance(event, SapBomAsBuiltSet):
            event_specific['Type'] = event.name()
            event_specific['Description'] = "SAP BOM as Built Set"
            event_specific['Details'] = []
        elif isinstance(event, SapEquipmentHistoryMixin):
            event_specific['Type'] = event.name()
            event_specific['Description'] = "SAP Equipment History"
            event_specific['Details'] = [{"EventName": "Description",
                                          "EventValue": item.get("Ktext", BaseView.NO_DATA_FROM_SOURCE)}]
            # add a list of document names and links
            attachments_list = self._create_sap_attachments_list(event.asset, item.get("Documents", []))
            event_specific['Attachments'] = attachments_list
        elif isinstance(event, TalendTimDocumentSet):
            event_specific['Type'] = event.name()
            event_specific['Description'] = 'Technical Document'

            summary = []
            for doc in item:
                description = doc.get('documentDescription')
                if not description:
                    continue
                parts = description.split(' ')
                if summary:
                    summary[-1] += ','
                summary.extend(parts[:4])
                if len(summary) > 4:
                    break

            if not summary:
                summary = BaseView.NO_DATA_FROM_SOURCE
            elif len(summary) > 4:
                summary = '{}...'.format(' '.join(summary[:4]))
            else:
                summary = ' '.join(summary)

            event_specific['Details'] = [
                {
                    "DocumentCount": len(item),
                    "DocumentSummary": summary
                }
            ]

            attachments_list = self._create_talend_attachments_list(
                event.asset, item)
            event_specific['Attachments'] = attachments_list
        elif isinstance(event, TalendFirmwareSet):
            event_specific['Type'] = event.name()
            event_specific['Description'] = "FSW Version"
            event_specific['Details'] = []
        elif isinstance(event, FieldDataErrorSet):
            event_specific['Type'] = event.name()
            event_specific['Description'] = "Field Data Error"
            blob_name, err_msg = self.extract_field_data_error(item)
            event_specific['Details'] = [
                {"EventName": "Error Message", "EventValue": err_msg},
                {"EventName": "Filename", "EventValue": blob_name}
            ]
        elif isinstance(event, SapWarrantyRecallSet):
            event_specific = self._create_kif_data(event, item)

        return event_specific
