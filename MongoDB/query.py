# Copyright (c) 2019 Rolls-Royce Power Systems AG. All rights reserved.

import datetime
import json
import logging
from os import path

import pymongo
from pymongo import MongoClient
import dateutil.parser

logger = logging.getLogger(__name__)


class DataAccess:

    CACHE_SIZE = 10000

    IGNORE_FIELDS = {'_id': False, '_last_field_data_update': False, '_clmno': False,
                     'asset_id': False, 'source': False, 'offset': False}

    def __init__(self, connection_string, database='practice_db'):
        self.connection_string = connection_string
        self.database = database
        self.client = None

    def open(self):
        self.client = MongoClient(self.connection_string)

    def remove_legacy_documents(self):
        database = self.client[self.database]
        database.doc_list.delete_many({"$and": [{"Size": {"$exists": False}}, {"Type": "TalendTimDocumentSet"}]})
        ron_docs = database.ron.find({"Type": "SapBomAsBuiltSet", "Description": "SAP BOM as Built Set"})
        for doc in ron_docs:
            creation_date = datetime.datetime.strptime(doc["Ts"][:10], "%Y-%m-%d").strftime("%d.%m.%Y")
            doc['Description'] = "BoM as built set"
            doc['Details'] = [{"Type": "IBASE as Built", "CreationDate": creation_date}]
            database.ron.replace_one({"_id": doc["_id"]}, doc, upsert=True)

    def check_inject_dummy_data(self):

        database = self.client[self.database]

        path_start = './sample_data'

        if database.bom.count() == 0:
            with open(path.join(path_start, 'Bom-A-9110100013.json'), 'r') as json_file:
                loaded_json = json.load(json_file)
                loaded_json['asset_id'] = "9110100013"
                database.bom.insert(loaded_json)

        if database.basic_data.count() == 0:
            with open(path.join(path_start, 'Basic-9110100013.json'), 'r') as json_file:
                loaded_json = json.load(json_file)
                loaded_json['asset_id'] = "9110100013"
                database.basic_data.insert(loaded_json)

        if database.ron.count() == 0:
            with open(path.join(path_start, 'RON-9110100013.json'), 'r') as json_file:
                loaded_json = json.load(json_file)

                for item in loaded_json:
                    item['asset_id'] = "9110100013"

                database.ron.insert(loaded_json)

        if database.field_data.count() == 0:
            with open(path.join(path_start, 'field-data.json'), 'r') as json_file:
                loaded_json = json.load(json_file)

                for item in loaded_json:
                    item['asset_id'] = "9110100013"

                database.field_data.insert(loaded_json)

        if database.doc_list.count() == 0:
            with open(path.join(path_start, 'doc-list.json'), 'r') as json_file:
                loaded_json = json.load(json_file)

                for item in loaded_json:
                    item['asset_id'] = "9110100013"

                database.doc_list.insert(loaded_json)

        if database.part_info.count() == 0:
            with open(path.join(path_start, 'part-info-9110100013.json'), 'r') as json_file:
                loaded_json = json.load(json_file)

                database.part_info.insert(loaded_json)

    def load_latest_asset_times(self, table_name):
        """ create a dictionary of assets and the latest update
            times for each assets
        """
        latest_times = {}

        try:
            database = self.client[self.database]

            asset_times = database[table_name].aggregate(
                [{"$group": {"_id": "$asset_id", "max_time": {"$max": "$Ts"}}}])

            for asset_time in asset_times:
                latest_times.update({int(asset_time["_id"]): dateutil.parser.parse(asset_time["max_time"])})

        except:  # pylint: disable=broad-except
            logger.exception("Failed loading latest asset times from table %s", table_name)
            raise

        return latest_times

    def save(self, table_name, asset_id, payload):
        """ saves the data raising exception if fails
            """
        try:
            database = self.client[self.database]

            if isinstance(payload, list):
                database[table_name].insert_many(payload)
            else:
                database[table_name].insert_one(payload)

            logger.debug("inserted new %s update for asset id %s", table_name, asset_id)
        except Exception:
            logger.exception("Failed inserting %s for asset id %s", table_name, asset_id)
            raise

    def remove(self, table_name, asset_id, key=None):
        """ remove all data relating to a key which defaults to asset from the views table """

        if not key:
            key = {"asset_id": asset_id}

        try:
            database = self.client[self.database]

            database[table_name].delete_many(key)

            logger.debug("removed data from %s for asset id %s", table_name, asset_id)
        except Exception:
            logger.exception("Failed removing data from %s for asset id %s", table_name, asset_id)
            raise

    def upsert(self, table_name, asset_id, payload, key=None):
        """ insert (or update if item already exists based on key which defaults to asset id)
            used to update basic data
        """
        if not key:
            key = {"asset_id": asset_id}

        try:
            database = self.client[self.database]

            database[table_name].replace_one(key, payload, upsert=True)

            logger.debug("upserted new %s update for asset id %s", table_name, asset_id)
        except Exception:
            logger.exception(
                "Failed upserting %s for asset id %s", table_name, asset_id)
            raise

    def load(self, table_name, asset_id, query=None, ignore_fields=None):
        """ load asset data from a table
        """
        if not query:
            query = {"asset_id": asset_id}

        try:
            database = self.client[self.database]

            results = database[table_name].find_one(query, ignore_fields)

            logger.debug("Load asset from %s for asset id %s", table_name, asset_id)
        except Exception:
            logger.exception("Failed loading asset from %s for asset id %s", table_name, asset_id)
            raise

        return results

    def do_housekeeping(self, table_name, limit_cache=CACHE_SIZE):
        """ keeps the size of the cache down
            if fails raises exception
        """
        try:
            database = self.client[self.database]

            assets_ids = database[table_name].distinct("asset_id")

            for asset_id in assets_ids:
                results = database[table_name].find({"asset_id": asset_id}).sort(
                    "Ts", pymongo.DESCENDING).limit(limit_cache + 1)

                res_list = list(results)

                if len(res_list) <= limit_cache:
                    continue  # not cache limit

                last_one = res_list[-1]

                database[table_name].remove({"Ts": {"$lte": last_one["Ts"]}, "asset_id": asset_id})

        except Exception:
            logger.exception("Failed housekeeping table %s", table_name)
            raise

    def close(self):
        if self.client:
            self.client.close()
            self.client = None

    def fetch_many(self, table_name, asset_id, ignore_fields, start=None, sort_field=None, stop=None,
                   order_desc=True, extra_filters=None, limit=None):
        """ given a table name and an optional start and stop date return a json response from the database
            ignore_fields are fields that shouldn't be returned in the result set
        """

        if not table_name:
            raise ValueError("Table name not provided")

        if not asset_id:
            raise ValueError("Expecting asset id")

        query = {}

        if sort_field and start and stop:
            query = {sort_field: {"$gte": start, "$lt": stop}}

        query.update({"asset_id": asset_id})

        if extra_filters:
            query.update(extra_filters)

        try:
            database = self.client[self.database]

            result_obj = database[table_name].find(query, ignore_fields)

            if sort_field:
                result_obj = result_obj.sort(sort_field, pymongo.DESCENDING if order_desc else pymongo.ASCENDING)

            if limit:
                result_obj = result_obj.limit(limit)

            return result_obj

        except Exception:
            logger.exception("Exception reading from table %s", table_name)
            raise

    def get_latest_update_time(self, table_name, asset_id):
        if not table_name:
            raise ValueError("Table name not provided")

        try:
            database = self.client[self.database]

            results = database[table_name].find({"asset_id": asset_id}).sort("Ts", pymongo.DESCENDING).limit(1)

            if results is None:
                return None

            result = None

            try:
                result = results.next()
            except StopIteration:
                pass

            if result is None:
                return None

            latest_time = dateutil.parser.parse(result["Ts"])

            return latest_time

        except Exception:
            logger.exception("get_latest_update_time for %s table asset id %s failed", table_name, asset_id)
            raise
