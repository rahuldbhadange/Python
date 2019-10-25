# Copyright (c) 2018 Rolls-Royce Power Systems AG. All rights reserved.


"""Saves Kif (correction in field) data from apWarrantyRecallSet event
"""

import logging
from pprint import pprint

from .BaseView import BaseView

logger = logging.getLogger(__name__)


class UpcomingEventsView(BaseView):

    def capture_old_data(self, event):

        try:
            return self._data_access.load(self.UPCOMING_EVENTS_DATA_TABLE, event.asset)
        except:  # pylint: disable broad-except
            logger.exception("Exception reading from table %s when capturing the old data", self.BASIC_DATA_TABLE)
            return None

    def on_event(self, event, old_data=None):
        logger.info("%s on_event called", self.__class__.__name__)

        payload = event.data
        print("\n\npayload\n\n\n")
        pprint(payload)
        print("\n\n\n\n\n")

        mapped_list, remove_list = self._map_list(event, payload, old_data)
        print("\n\nmapped_list\n\n\n")
        pprint(mapped_list)
        print("\n\n\n\n\n")
        print("\n\nremove_list\n\n\n")
        pprint(remove_list)
        print("\n\n\n\n\n")

        for item in mapped_list:
            self._data_access.upsert(self.UPCOMING_EVENTS_DATA_TABLE,
                                     event.asset, item, key={"_clmno": item['_clmno'], "asset_id": event.asset})

        # remove items that have been closed
        for remove_item in remove_list:
            self._data_access.remove(
                self.UPCOMING_EVENTS_DATA_TABLE, event.asset, remove_item)

    def _map_list(self, event, items, old_data):
        update_list = []
        remove_list = []

        for item in items:
            print("\n\nitem\n\n\n")
            pprint(item)
            print("\n\n\n\n\n")
            clmno = item.get("Clmno", "")
            AssetType = item.get("AssetType", "")
            old_Seq = old_data.get("Seq", "")
            current_Seq = event.offset
            print("\n\n\n\n\n")
            pprint(AssetType)
            pprint(current_Seq)
            pprint(old_Seq)
            pprint(clmno)
            print("\n\n\n\n\n")
            if self._is_kif_item_closed(item) and AssetType == "ENG" and old_Seq != current_Seq:
                clmno = item.get("Clmno", "")
                AssetType = item.get("AssetType", "")
                old_Seq = old_data.get("Seq", "")
                current_Seq = event.offset
                print("\n\n\n\n\n")
                pprint(AssetType)
                pprint(current_Seq)
                pprint(old_Seq)
                pprint(clmno)
                print("\n\n\n\n\n")
                # if old_data:
                #     old_Seq = old_data.get("Seq", "")
                # else:
                #     old_Seq = None

                if not clmno:
                    raise ValueError("keying off Clmno for kif data but field missing")

                # this item has been closed so remove from upcoming events
                remove_list.append({"asset_id": event.asset, "_clmno": clmno})

                # if AssetType == "ENG":

                # if AssetType == "ENG" and old_Seq != current_Seq:  # old.event.offset ??
                    # remove_list.append({"Seq": old_Seq})   # how to delete whole event wrt event.offset != old.event.offset
                    # print("##########")
                continue

            mapped_item = self._create_kif_data(event, item)
            update_list.append(mapped_item)

        return update_list, remove_list

