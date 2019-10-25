# Copyright (c) 2019 Rolls-Royce Power Systems AG. All rights reserved.

import json
import logging
import datetime
import dateutil.parser
from flask import request, Response, make_response, current_app, stream_with_context
from bson.json_util import dumps

from ioticlabs.dt.api.follower import (
    T2ResponseException, AssetUnknown, T2ReqFailureReason, T2Unavailable,
    T2Timeout, ShutdownRequested, NotConnected
)

from rrps.dt.follower.rest_follower.DataAccess import DataAccess
from rrps.dt.follower.rest_follower.auth import requires_auth
from rrps.dt.follower.rest_follower.views import BaseView, BOMAsBuiltView

logger = logging.getLogger(__name__)


"""An explicit list of event names that can be used in query filters.
"""
ALLOWED_FILTER_EVENT_NAMES = (
    'TalendTimDocumentSet',
)


class BadRequest(Exception):
    """ Format error response and append status code.
    """

    def __init__(self, error, status_code):
        super().__init__(error)
        self.error = error
        self.status_code = status_code


class InternalServerError(Exception):
    """ Format error response and append status code.
    """

    def __init__(self, error, status_code):
        super().__init__(error)
        self.error = error
        self.status_code = status_code


class NotFound(Exception):

    def __init__(self):
        super().__init__()
        self.error = "Document not found"
        self.status_code = 404


def _get_data_access():
    return DataAccess(current_app.config['connection_string'], current_app.config['database'])


def _add_newfields_and_load(table_name, asset_id):
    data_access = _get_data_access()

    try:
        data_access.open()

        result_obj = data_access.load(table_name, asset_id, ignore_fields=DataAccess.IGNORE_FIELDS)
        if not result_obj:
            result_obj = {}
        else:
            result_obj.update({"NewFields": []})

        start_time = datetime.datetime.utcnow() - datetime.timedelta(hours=24)
        start_time_isoformat = start_time.replace(microsecond=0).isoformat()

        extra_filters = {"Description": {"$in": ["Master Data Change", "FSW Version"]},
                         "Ts": {"$gt": start_time_isoformat}}

        ron_docs = data_access.fetch_many(BaseView.RON_DATA_TABLE, asset_id, DataAccess.IGNORE_FIELDS,
                                          sort_field="Ts", extra_filters=extra_filters)

        if result_obj and ron_docs:
            result_obj["NewFields"] = {doc['FieldName'] for doc in ron_docs}

        # use bson
        result = dumps(result_obj)

        # remove escaped quotes
        resp = make_response(result)
        resp.headers["Content-Type"] = "application/json"

        return resp
    except Exception:
        logger.exception("querying %s table failed", table_name)
        raise
    finally:
        data_access.close()


def _load(table_name, asset_id):
    """ load single result set from the database """

    data_access = _get_data_access()

    try:
        data_access.open()

        result_obj = data_access.load(table_name, asset_id, ignore_fields=DataAccess.IGNORE_FIELDS)

        if not result_obj:
            result_obj = {}

        # use bson
        result = dumps(result_obj)

        # remove escaped quotes
        resp = make_response(result)
        resp.headers["Content-Type"] = "application/json"

        return resp
    except Exception:
        logger.exception("querying %s table failed", table_name)
        raise
    finally:
        data_access.close()


def _load_values(table_name, asset_id, sort_field=None, start=None, stop=None, descending=True, extra_filters=None,
                 limit=None):
    """ fetch multiple rows from the database """
    converted_start = None
    converted_stop = None

    # convert compressed iso times to python
    if start and stop:
        converted_start, converted_stop = _parse_start_and_stop_times(
            start, stop)

    data_access = _get_data_access()

    try:
        data_access.open()

        result_obj = data_access.fetch_many(
            table_name, asset_id, DataAccess.IGNORE_FIELDS, start=converted_start,
            sort_field=sort_field, stop=converted_stop, order_desc=descending, extra_filters=extra_filters, limit=limit,
        )

        # use bson
        result = dumps(result_obj)

        # remove escaped quotes
        resp = make_response(result)
        resp.headers["Content-Type"] = "application/json"

        return resp
    except Exception:
        logger.exception("querying %s table failed", table_name)
        raise
    finally:
        data_access.close()


def _parse_start_and_stop_times(start, stop):
    """ convert compressed iso time "20181009T160920Z" to
    uncompressed times 2018-10-09T16:09:20+00:00
    """
    try:
        start_time = dateutil.parser.parse(start)
        stop_time = dateutil.parser.parse(stop)

        if start_time >= stop_time:
            raise ValueError("Stop time must be after start time")

        converted_start_time = start_time.isoformat()
        converted_stop_time = stop_time.isoformat()
    except ValueError as ex:
        logger.exception("parse stop and start failed")
        raise BadRequest({"code": "parse stop and start failed", "description": str(
            ex)}, status_code=400)
    except Exception:
        message = "Failed to find convert stop ({}) or start ({}) time".format(
            start, stop)
        logger.exception(message)
        raise BadRequest({"code": "parse stop and start failed",
                          "description": message}, status_code=400)

    return converted_start_time, converted_stop_time


@requires_auth
def get_field_data_by_asset_id(asset_id):  # noqa: E501
    """Find field data by asset ID.
    """
    data_access = _get_data_access()

    try:
        data_access.open()

        latest_time = data_access.get_latest_update_time(BaseView.FIELD_DATA_TABLE, asset_id)
    finally:
        data_access.close()

    if latest_time is None:
        resp = make_response("[]")
        resp.headers["Content-Type"] = "application/json"
        return resp

    # get the last 15 minutes of data
    end_time = latest_time
    start_time = end_time - datetime.timedelta(minutes=15)

    start_time_iso = start_time.strftime("%Y%m%dT%H%M%SZ")
    end_time_iso = end_time.strftime("%Y%m%dT%H%M%SZ")

    return get_field_data_by_asset_id_and_time(asset_id, start_time_iso, end_time_iso)


@requires_auth
def get_field_data_by_asset_id_and_time(asset_id, start, stop):  # pylint: disable=invalid-name
    """Find field data by asset ID and time.

    :param asset_id: the ID of the asset.

    :param start: start time in format YYYYmmDDTHHMMSSZ e.g. 20181009T160856Z
    :param end: end time, results returned up to but not including this time in format YYYYmmDDTHHMMSSZ

    :rtype: None
    """
    return _load_values(BaseView.FIELD_DATA_TABLE, asset_id, sort_field="Ts", start=start, stop=stop)


@requires_auth
def get_bom_data_by_asset_id(asset_id):  # pylint: disable=invalid-name
    """Find bom as built data by asset ID and time.

    : param asset_id: ID asset to return

    : param start: start time in format YYYYmmDDTHHMMSSZ e.g. 20181009T160856Z
    : param end: end time, results returned up to but not including this time in format YYYYmmDDTHHMMSSZ

    : rtype: None
    """

    return _load(BaseView.BOM_DATA_TABLE, asset_id)


@requires_auth
def get_ron_data_by_asset_id_and_time(asset_id, start, stop):  # pylint: disable=invalid-name
    """Get River of News data by asset id

    Returns a single asset

    : param asset_id: ID asset to return

    : param start: start time in format YYYYmmDDTHHMMSSZ e.g. 20181009T160856Z
    : param end: end time, results returned up to but not including this time in format YYYYmmDDTHHMMSSZ

    : rtype: None
    """
    return _load_values(BaseView.RON_DATA_TABLE, asset_id, sort_field="Ts", start=start, stop=stop, descending=True)


@requires_auth
def get_ron_data_by_asset_id(asset_id):  # pylint: disable=invalid-name
    """Get River of News data by asset id

    Returns a single asset

    : param asset_id: ID asset to return

    : rtype: None
    """
    return get_ron_data_by_asset_id_and_time(asset_id, None, None)


@requires_auth
def get_weather_info_by_asset_id(asset_id):
    """Returns weather information for the specified asset.
    """
    return _load(BaseView.WEATHER_INFO_TABLE, asset_id)


@requires_auth
def get_basic_data_by_asset_id(asset_id):  # pylint: disable=invalid-name
    """Find basic data aka StammDaten by asset ID

    Returns a single asset

    : param asset_id: ID asset to return

    : rtype: None
    """

    return _add_newfields_and_load(BaseView.BASIC_DATA_TABLE, asset_id)


@requires_auth
def get_master_field_history_by_asset_id(asset_id, field_name):  # pylint: disable=invalid-name
    """Get the historical values for a field name.
    """
    limit = request.args.get('limit')
    if limit:
        limit = int(limit)

    data_access = _get_data_access()

    try:
        response_obj = {"FieldName": field_name,
                        "Values": []}
        data_access.open()

        extra_filters = {"FieldName": field_name,
                         "Description": {"$in": ["Master Data Change", "FSW Version"]}}

        ron_docs = data_access.fetch_many(BaseView.RON_DATA_TABLE, asset_id, DataAccess.IGNORE_FIELDS,
                                          sort_field="Ts", extra_filters=extra_filters, limit=limit)

        if ron_docs:
            value_list = [{"Ts": doc["Ts"], "FieldValue": doc["FieldNewValue"]} for doc in ron_docs]
            response_obj["Values"] = value_list

        # use bson
        result = dumps(response_obj)

        # remove escaped quotes
        resp = make_response(result)
        resp.headers["Content-Type"] = "application/json"

        return resp
    except Exception:
        logger.exception("Querying table %s failed", BaseView.RON_DATA_TABLE)
        raise
    finally:
        data_access.close()


@requires_auth
def get_bom_as_maintained_by_asset_id(asset_id):  # pylint: disable=invalid-name
    """Get latest bom as maintained for an asset id.
    """

    follower = current_app.config['follower']

    mime_type = ""
    json_data = '{}'

    try:
        encoded_data = []

        for mime_type, chunk in follower.request_bom_as_maintained(asset_id, datetime.datetime.now()):
            encoded_data.extend(chunk)

        if mime_type.lower() != 'application/json':
            raise ValueError("Expected mime type of json by didnt received it")

        decoded_bom_data = bytes(encoded_data).decode('utf-8')
        reordered_data = BOMAsBuiltView.bom_to_tree(asset_id, json.loads(decoded_bom_data))

        utc_time = reordered_data[0].get("ValidFrom", "")

        bom = {"Ts": utc_time, "Materials": reordered_data}

        json_data = json.dumps(bom)

    except AssetUnknown:
        msg = 'T2 - Asset {} no longer known, ignoring'.format(asset_id)
        logger.warning(msg)
    except T2ResponseException as ex:
        # ex.reason is T2ReqFailureReason - see code documentation for what they mean
        if ex.reason == T2ReqFailureReason.REQ_UNHANDLED:
            logger.error('T2 request not handled by provider')
        # equivalent to HTTP 404
        elif ex.reason == T2ReqFailureReason.RESOURCE_UNKNOWN:
            logger.error('Data not available for given request and asset')
        else:
            logger.error('T2 failed - reason: %s', ex.reason)

        if ex.reason != T2ReqFailureReason.RESOURCE_UNKNOWN:
            raise InternalServerError({"code": "failed requesting BOM", "description": str(ex)}, status_code=500)
    except T2Unavailable as ex:
        msg = 'T2 functionality not enabled in follower'
        logger.critical(msg)
        raise InternalServerError({"code": msg, "description": str(ex)}, status_code=500)
    except T2Timeout as ex:
        msg = 'T2 request timed out'
        logger.error(msg)
        raise InternalServerError({"code": msg, "description": str(ex)}, status_code=500)
    except ShutdownRequested as ex:
        msg = 'The follower is shutting down'
        logger.error(msg)
        raise InternalServerError({"code": msg, "description": str(ex)}, status_code=500)
    except NotConnected as ex:
        msg = 'The follower temporarily lost connection to the T2 providers'
        logger.error(msg)
        raise InternalServerError({"code": msg, "description": str(ex)}, status_code=500)
    except Exception as ex:
        msg = 'T2 failure fetching bom asset_id {}'.format(
            asset_id)
        raise InternalServerError({"code": msg, "description": str(ex)}, status_code=500)

    return Response(json_data, mimetype=mime_type)


@requires_auth
def get_doc_list_by_asset_id(asset_id):  # noqa: E501
    """Returns the document list for the specified asset_id.
    """
    event_name = request.args.get('event')

    extra_filters = {}
    if event_name and event_name in ALLOWED_FILTER_EVENT_NAMES:
        extra_filters['Type'] = event_name

    return _load_values(BaseView.DOC_LIST_TABLE, asset_id, extra_filters=extra_filters)


def _map_current_part_info(current_part_info):
    """ returns current part info in the format expected by UI """
    part_info = {
        "Batch": BaseView.NO_DATA_FROM_SOURCE,
        "Consumables": [
            {
                "ConsumableName": BaseView.NO_DATA_FROM_SOURCE
            }
        ],
        "Depth": BaseView.NO_DATA_FROM_SOURCE,
        "EmmissionRelevant": BaseView.NO_DATA_FROM_SOURCE,
        "InstalledDate": BaseView.NO_DATA_FROM_SOURCE,
        "Length": "{} {}".format(current_part_info.get('Laeng', BaseView.NO_DATA_FROM_SOURCE),
                                 current_part_info.get('Meabm', BaseView.NO_DATA_FROM_SOURCE)),
        "MaterialId": BaseView.NO_DATA_FROM_SOURCE,
        "MaterialNumber": current_part_info.get('Matnr', BaseView.NO_DATA_FROM_SOURCE),
        "PartId": BaseView.NO_DATA_FROM_SOURCE,
        "PartName": BaseView.NO_DATA_FROM_SOURCE,
        "Parts": [
            {
                "PartName": BaseView.NO_DATA_FROM_SOURCE
            }],
        "PreviousPartInstalledDate": BaseView.NO_DATA_FROM_SOURCE,
        "PreviousPartName": BaseView.NO_DATA_FROM_SOURCE,
        "SerialNumber": BaseView.NO_DATA_FROM_SOURCE,
        "Tools": [
            {
                "ToolName": BaseView.NO_DATA_FROM_SOURCE
            }
        ],
        "Weight": "{} {}".format(current_part_info.get('Ntgew', BaseView.NO_DATA_FROM_SOURCE),
                                 current_part_info.get('Gewei', BaseView.NO_DATA_FROM_SOURCE)),
        "Width": "{} {}".format(current_part_info.get('Breit', BaseView.NO_DATA_FROM_SOURCE),
                                current_part_info.get('Meabm', BaseView.NO_DATA_FROM_SOURCE)),
        "Link": BaseView.NO_DATA_FROM_SOURCE,
        "Source": "SAP"
    }

    return part_info


@requires_auth
def get_part_info_by_material_id(asset_id, material_id):
    """ Get part info by material id
    """
    follower = current_app.config['follower']

    mime_type = ""
    part_info_json_data = "{}"

    try:
        encoded_data = []
        for mime_type, chunk in follower.request_part_info(asset_id, material_id):
            encoded_data.extend(chunk)

        if mime_type.lower() != 'application/json':
            raise ValueError(
                "Expected mime type of application/json by didnt received it")

        json_data = bytes(encoded_data).decode('utf-8')
        decoded_data = json.loads(json_data)

        if not decoded_data:
            raise TypeError("Expecting a non empty dictionary with current part info and substitute part info")

        part_info_json_data = json.dumps(decoded_data)

    except AssetUnknown:
        msg = 'T2 - Asset {} no longer known, ignoring'.format(asset_id)
        logger.warning(msg)
    except T2ResponseException as ex:
        # ex.reason is T2ReqFailureReason - see code documentation for what they mean
        if ex.reason == T2ReqFailureReason.REQ_UNHANDLED:
            logger.error('T2 request not handled by provider')
        # equivalent to HTTP 404
        elif ex.reason == T2ReqFailureReason.RESOURCE_UNKNOWN:
            logger.error('Data not available for given request and asset')
        else:
            logger.error('T2 failed - reason: %s', ex.reason)

        if ex.reason != T2ReqFailureReason.RESOURCE_UNKNOWN:
            raise InternalServerError({"code": "failed requesting part info", "description": str(
                ex)}, status_code=500)
    except T2Unavailable as ex:
        msg = 'T2 functionality not enabled in follower'
        logger.critical(msg)
        raise InternalServerError({"code": msg, "description": str(
            ex)}, status_code=500)
    except T2Timeout as ex:
        msg = 'T2 request timed out'
        logger.error(msg)
        raise InternalServerError({"code": msg, "description": str(
            ex)}, status_code=500)
    except ShutdownRequested as ex:
        msg = 'The follower is shutting down'
        logger.error(msg)
        raise InternalServerError({"code": msg, "description": str(
            ex)}, status_code=500)
    except NotConnected as ex:
        msg = 'The follower temporarily lost connection to the T2 providers'
        logger.error(msg)
        raise InternalServerError({"code": msg, "description": str(
            ex)}, status_code=500)
    except Exception as ex:
        msg = 'T2 failure fetching part info material_id {}'.format(
            material_id)
        raise InternalServerError({"code": msg, "description": str(
            ex)}, status_code=500)

    try:
        return Response(part_info_json_data, mimetype=mime_type)
    except Exception:
        logger.exception("get part info by material id")
        raise


@requires_auth
def get_part_info_history_by_material_id(asset_id, material_id):  # pylint: disable=invalid-name
    """ Get part info history by material id
    """
    follower = current_app.config['follower']

    mime_type = ""
    part_info_history_json_data = "{}"

    try:
        encoded_data = []
        for mime_type, chunk in follower.request_part_info_history(asset_id, material_id):
            encoded_data.extend(chunk)

        if mime_type.lower() != 'application/json':
            raise ValueError(
                "Expected mime type of application/json by didnt received it")

        json_data = bytes(encoded_data).decode('utf-8')

        decoded_data = json.loads(json_data)
        if not decoded_data:
            raise TypeError("Expecting an array with current part info history")

        part_info_history = {'Sorted_Parts': decoded_data}
        part_info_history_json_data = json.dumps(part_info_history)

    except AssetUnknown:
        msg = 'T2 - Asset {} no longer known, ignoring'.format(asset_id)
        logger.warning(msg)
    except T2ResponseException as ex:
        # ex.reason is T2ReqFailureReason - see code documentation for what they mean
        if ex.reason == T2ReqFailureReason.REQ_UNHANDLED:
            logger.error('T2 request not handled by provider')
        # equivalent to HTTP 404
        elif ex.reason == T2ReqFailureReason.RESOURCE_UNKNOWN:
            logger.error('Data not available for given request and asset')
        else:
            logger.error('T2 failed - reason: %s', ex.reason)

        if ex.reason != T2ReqFailureReason.RESOURCE_UNKNOWN:
            raise InternalServerError({"code": "failed requesting part info", "description": str(
                ex)}, status_code=500)
    except T2Unavailable as ex:
        msg = 'T2 functionality not enabled in follower'
        logger.critical(msg)
        raise InternalServerError({"code": msg, "description": str(ex)}, status_code=500)
    except T2Timeout as ex:
        msg = 'T2 request timed out'
        logger.error(msg)
        raise InternalServerError({"code": msg, "description": str(ex)}, status_code=500)
    except Exception as ex:
        msg = 'T2 failure fetching part info material_id {}'.format(material_id)
        raise InternalServerError({"code": msg, "description": str(ex)}, status_code=500)

    try:
        return Response(part_info_history_json_data, mimetype=mime_type)
    except Exception:
        logger.exception("get part info by material id")
        raise


@requires_auth
def get_document_by_id(asset_id, document_id, file_ext):
    """Get document using document id.
    """
    follower = current_app.config['follower']

    mime_type = ""
    first_chunk = None

    iterator = iter(follower.request_sap_document(asset_id, document_id))

    try:
        mime_type, first_chunk = next(iterator)
    except AssetUnknown:
        logger.warning('T2 - Asset %s no longer known, ignoring', asset_id)
        raise NotFound()
    except T2ResponseException as ex:
        if ex.reason == T2ReqFailureReason.REQ_UNHANDLED:
            logger.error('T2 request not handled by provider')
        elif ex.reason == T2ReqFailureReason.RESOURCE_UNKNOWN:
            logger.error('Data not available for given request and asset')
            raise NotFound()
        else:
            logger.error('T2 failed - reason: %s', ex.reason)
        raise InternalServerError({"code": "failed requesting document", "description": str(ex)}, status_code=500)
    except T2Unavailable as ex:
        msg = 'T2 functionality not enabled in follower'
        logger.critical(msg)
        raise InternalServerError({"code": msg, "description": str(ex)}, status_code=500)
    except T2Timeout as ex:
        msg = 'T2 request timed out'
        logger.error(msg)
        raise InternalServerError({"code": msg, "description": str(ex)}, status_code=500)
    except ShutdownRequested as ex:
        msg = 'The follower is shutting down'
        logger.error(msg)
        raise InternalServerError({"code": msg, "description": str(ex)}, status_code=500)
    except NotConnected as ex:
        msg = 'The follower temporarily lost connection to the T2 providers'
        logger.error(msg)
        raise InternalServerError({"code": msg, "description": str(ex)}, status_code=500)
    except Exception as ex:
        msg = 'T2 failure fetching sap document'
        raise InternalServerError({"code": msg, "description": str(ex)}, status_code=500)

    @stream_with_context
    def generate():
        try:
            yield first_chunk
            for _, next_chunk in iterator:
                yield next_chunk
        except T2Timeout as ex:
            msg = 'T2 request timed out'
            logger.error(msg)
            raise InternalServerError({"code": msg, "description": str(ex)}, status_code=500)
        except ShutdownRequested as ex:
            msg = 'The follower is shutting down'
            logger.error(msg)
            raise InternalServerError({"code": msg, "description": str(ex)}, status_code=500)
        except NotConnected as ex:
            msg = 'The follower temporarily lost connection to the T2 providers'
            logger.error(msg)
            raise InternalServerError({"code": msg, "description": str(ex)}, status_code=500)
        except Exception as ex:
            msg = 'T2 failure fetching sap document'
            raise InternalServerError({"code": msg, "description": str(ex)}, status_code=500)

    try:
        response = Response(generate(), mimetype=mime_type)
        response.headers['Content-Disposition'] = 'attachment; filename="{}.{}"'.format(document_id, file_ext)
        return response
    except Exception:
        logger.exception("get document by id failed")
        raise


@requires_auth
def get_talend_document_by_id(asset_id, document_label, document_name):
    """ Get a talend document
    """

    follower = current_app.config['follower']

    mime_type = ""
    first_chunk = None

    iterator = iter(follower.request_talend_document(asset_id, document_label, document_name))

    try:
        mime_type, first_chunk = next(iterator)
    except AssetUnknown:
        msg = 'T2 - Asset {} no longer known, ignoring'.format(asset_id)
        logger.warning(msg)
        raise NotFound()
    except T2ResponseException as ex:
        # ex.reason is T2ReqFailureReason - see code documentation for what they mean
        if ex.reason == T2ReqFailureReason.REQ_UNHANDLED:
            logger.error('T2 request not handled by provider')
        # equivalent to HTTP 404
        elif ex.reason == T2ReqFailureReason.RESOURCE_UNKNOWN:
            logger.error('Data not available for given request and asset')
            raise NotFound()
        else:
            logger.error('T2 failed - reason: %s', ex.reason)

        raise InternalServerError({"code": "failed requesting document", "description": str(
            ex)}, status_code=500)
    except T2Unavailable as ex:
        msg = 'T2 functionality not enabled in follower'
        logger.critical(msg)
        raise InternalServerError({"code": msg, "description": str(
            ex)}, status_code=500)
    except T2Timeout as ex:
        msg = 'T2 request timed out'
        logger.error(msg)
        raise InternalServerError({"code": msg, "description": str(
            ex)}, status_code=500)
    except ShutdownRequested as ex:
        msg = 'The follower is shutting down'
        logger.error(msg)
        raise InternalServerError({"code": msg, "description": str(
            ex)}, status_code=500)
    except NotConnected as ex:
        msg = 'The follower temporarily lost connection to the T2 providers'
        logger.error(msg)
        raise InternalServerError({"code": msg, "description": str(
            ex)}, status_code=500)
    except Exception as ex:
        msg = 'T2 failure fetching document'
        raise InternalServerError({"code": msg, "description": str(
            ex)}, status_code=500)

    @stream_with_context
    def generate():
        try:
            yield first_chunk
            for _, next_chunk in iterator:
                yield next_chunk
        except T2Timeout as ex:
            msg = 'T2 request timed out'
            logger.error(msg)
            raise InternalServerError({"code": msg, "description": str(
                ex)}, status_code=500)
        except ShutdownRequested as ex:
            msg = 'The follower is shutting down'
            logger.error(msg)
            raise InternalServerError({"code": msg, "description": str(
                ex)}, status_code=500)
        except NotConnected as ex:
            msg = 'The follower temporarily lost connection to the T2 providers'
            logger.error(msg)
            raise InternalServerError({"code": msg, "description": str(
                ex)}, status_code=500)
        except Exception as ex:
            msg = 'T2 failure fetching document'
            raise InternalServerError({"code": msg, "description": str(
                ex)}, status_code=500)

    try:
        response = Response(generate(), mimetype=mime_type)
        response.headers['Content-Disposition'] = 'attachment; filename="{}"'.format(
            document_name)
        return response
    except Exception:
        logger.exception("get document by id failed")
        raise


def get_status():
    """ Returns status of api """
    status = current_app.config.get('status', {})
    resp = make_response(json.dumps(status))
    resp.headers["Content-Type"] = "application/json"
    return resp


def get_root():
    """ Returns status of api """
    return get_status()


@requires_auth
def get_upcoming_events_by_id(asset_id):
    """ Get upcoming events using asset id
    """
    return _load_values(BaseView.UPCOMING_EVENTS_DATA_TABLE, asset_id, sort_field="Ts", descending=False)

@requires_auth
def get_document_by_type(asset_id, document_type):
    """Get document using document id.
    """
    follower = current_app.config['follower']

    mime_type = ""
    first_chunk = None

    # iterator = iter(follower.request_sap_document_type(asset_id, document_type))

    try:
        encoded_data = []

        for mime_type, chunk in follower.request_sap_document_type(asset_id, document_type):
            encoded_data.extend(chunk)

        json_data = bytes(encoded_data).decode('utf-8')
        decoded_data = json.loads(json_data)

        if not isinstance(decoded_data, list) or not decoded_data:
            raise TypeError("Expecting an array with current part info and substitute part info")

        for part_info in decoded_data:
            file_name = part_info['FileName']
            first_chunk = part_info['Xstring']
        # mime_type, first_chunk = next(iterator)

    except AssetUnknown:
        logger.warning('T2 - Asset %s no longer known, ignoring', asset_id)
        raise NotFound()
    except T2ResponseException as ex:
        if ex.reason == T2ReqFailureReason.REQ_UNHANDLED:
            logger.error('T2 request not handled by provider')
        elif ex.reason == T2ReqFailureReason.RESOURCE_UNKNOWN:
            logger.error('Data not available for given request and asset')
            raise NotFound()
        else:
            logger.error('T2 failed - reason: %s', ex.reason)
        raise InternalServerError({"code": "failed requesting document", "description": str(ex)}, status_code=500)
    except T2Unavailable as ex:
        msg = 'T2 functionality not enabled in follower'
        logger.critical(msg)
        raise InternalServerError({"code": msg, "description": str(ex)}, status_code=500)
    except T2Timeout as ex:
        msg = 'T2 request timed out'
        logger.error(msg)
        raise InternalServerError({"code": msg, "description": str(ex)}, status_code=500)
    except ShutdownRequested as ex:
        msg = 'The follower is shutting down'
        logger.error(msg)
        raise InternalServerError({"code": msg, "description": str(ex)}, status_code=500)
    except NotConnected as ex:
        msg = 'The follower temporarily lost connection to the T2 providers'
        logger.error(msg)
        raise InternalServerError({"code": msg, "description": str(ex)}, status_code=500)
    except Exception as ex:
        msg = 'T2 failure fetching sap document'
        raise InternalServerError({"code": msg, "description": str(ex)}, status_code=500)

    @stream_with_context
    def generate():
        try:
            yield first_chunk
            # for _, next_chunk in iterator:
            #     yield next_chunk
        except T2Timeout as ex:
            msg = 'T2 request timed out'
            logger.error(msg)
            raise InternalServerError({"code": msg, "description": str(ex)}, status_code=500)
        except ShutdownRequested as ex:
            msg = 'The follower is shutting down'
            logger.error(msg)
            raise InternalServerError({"code": msg, "description": str(ex)}, status_code=500)
        except NotConnected as ex:
            msg = 'The follower temporarily lost connection to the T2 providers'
            logger.error(msg)
            raise InternalServerError({"code": msg, "description": str(ex)}, status_code=500)
        except Exception as ex:
            msg = 'T2 failure fetching sap document'
            raise InternalServerError({"code": msg, "description": str(ex)}, status_code=500)

    try:
        response = Response(generate(), mimetype=mime_type)
        response.headers['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
        print("\n\nresponse\n", response)
        print("\n\n")
        return response
    except Exception:
        logger.exception("get document by type failed")
        raise
