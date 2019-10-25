# Copyright (c) 2018 Rolls-Royce Power Systems AG. All rights reserved.

"""Saves BOM as built updates
"""

import logging
from datetime import datetime
import pytz

from .BaseView import BaseView

logger = logging.getLogger(__name__)


class BOMAsBuiltView(BaseView):

    def on_event(self, event):
        logger.debug("%s on_event called asset_id %s", self.__class__.__name__, event.asset)

        # this reorders the flat data into a tree of materials
        bom_as_tree = BOMAsBuiltView.bom_to_tree(event.asset, event.data)

        if bom_as_tree:
            utc_time = bom_as_tree[0].get("ValidFrom", "")

            bom = {"asset_id": event.asset, "source": event.source,
                   "offset": event.offset, "Ts": utc_time, "Materials": bom_as_tree}

            self._data_access.upsert(self.BOM_DATA_TABLE, event.asset, bom)

    @staticmethod
    def bom_to_tree(asset_id, raw_data):
        """ given raw data as a flat list of materials
        return a tree where child materials are added to a list on their parent materials
        also removes some fields we dont use

        input:
            parent 1
            parent 2
            child 1 of parent 1
            child 2 of parent 1
            child 1 of parent 2

        output
            parent 1
                Children: [child 1 of parent 1, child 2 of parent 1]
            parent 2
                Children: [child 1 of parent 2]

        """

        # top level list of items
        materials = []

        # look up of item id to item
        id_to_item_map = {}

        # child items not associated with a parent yet
        orphans = {}

        raw_data = sorted(raw_data, key=lambda r: r.get('Sortf', ''))

        for item_in in raw_data:
            item = {}

            # items with this SonRecno value set as their ParRecno are children of this item
            child_id = item_in['SonRecno']
            parent_id = item_in['ParRecno']

            item['MaterialNumber'] = item_in.get("Matnr", BaseView.NO_DATA_FROM_SOURCE)
            item['Descr'] = item_in.get("Descr", BaseView.NO_DATA_FROM_SOURCE)
            item['BatchNumber'] = item_in.get("BatchNumber", BaseView.NO_DATA_FROM_SOURCE)
            item['SortField'] = item_in.get("Sortf")
            item['SerialNumber'] = item_in.get("Sernr", BaseView.NO_DATA_FROM_SOURCE)
            item['EmissionRelevance'] = item_in.get("Yyemrel", BaseView.NO_DATA_FROM_SOURCE)
            item['Amount'] = item_in.get("Amount")
            item['Unit'] = item_in.get("Unit")
            item['DateofRecord'] = item_in.get("Yydatum", BaseView.NO_DATA_FROM_SOURCE)
            item['MainGroup'] = item_in.get("Yyfkgrp")
            item['SubGroup'] = item_in.get("Yyfgrsp")

            # if this is a top level item then we want to get the valid from
            # time from it to give to the UI as the date that the BOM was built
            if not parent_id:
                valid_from = ""
                valid_from_str = item_in.get("Valfr", "")

                if valid_from_str:
                    valid_from_dt = datetime.strptime(
                        valid_from_str, "%Y%m%d%H%M%S")
                    valid_from_utc = pytz.utc.localize(valid_from_dt)
                    valid_from = valid_from_utc.isoformat()

                item['ValidFrom'] = valid_from

            if child_id:
                if child_id in id_to_item_map:
                    raise ValueError  # not expecting the same child_id more than once

                id_to_item_map[child_id] = item

            # add this item to its parent if it has one
            if parent_id:
                if parent_id in id_to_item_map:
                    parent_item = id_to_item_map[parent_id]
                    child_list = []
                    try:
                        child_list = parent_item['Children']
                    except KeyError:
                        parent_item['Children'] = child_list

                    child_list.append(item)
                else:
                    orphan_list = []
                    try:
                        orphan_list = orphans[parent_id]
                    except KeyError:
                        orphans[parent_id] = orphan_list

                    orphan_list.append(item)
            else:
                # top level item
                materials.append(item)

            # add any orphan children that belong to this parent
            if child_id in orphans:
                child_list = []
                try:
                    child_list = item['Children']
                except KeyError:
                    item['Children'] = child_list

                child_list.extend(orphans[child_id])

                orphans.pop(child_id)

        if orphans.keys():
            logger.warning("_bom_to_tree: Some material items did not have a parent item, asset id: %s", asset_id)

        if raw_data and not materials:
            logger.error("_bom_to_tree: no top level parent items in the raw data, asset id: %s", asset_id)

        return materials
