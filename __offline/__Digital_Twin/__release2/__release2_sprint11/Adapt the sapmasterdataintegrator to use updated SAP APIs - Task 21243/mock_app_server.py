import json
from flask import Flask, request, jsonify, abort
from werkzeug.exceptions import HTTPException
from flask_httpauth import HTTPBasicAuth
from cfg.config import Config

APP = Flask(__name__)
AUTH = HTTPBasicAuth()


@AUTH.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return Config.USER_DATA.get(username) == password


@APP.errorhandler(Exception)
def handle_error(exception):
    code = 500
    if isinstance(exception, HTTPException):
        code = exception.code
    return jsonify(error=str(exception)), code


def read_json(asset_id, mock_data_source):
    try:
        mock_data_file = mock_data_source + asset_id + ".json"
        with open(mock_data_file, mode="r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except:
        abort(404)


@APP.route('/')
def mock_api():
    return "mock api"


@APP.route("/sapmasterdata/hierarchy/<asset_id>", methods=["GET"])
# @APP.route("/sapmasterdata/hierarchy/$filter=Sernr%20eq%20{asset_id}&?format=json", methods=["GET"])
@AUTH.login_required
def get_sapmasterdata_hierarchy(asset_id):
    try:
        if request.method == 'GET':
            if asset_id:
                data = read_json(asset_id, Config.mock_data_source_sapmasterdata_hierarchy)
                return jsonify(data), 200
            abort(404)
        return None
    except:
        abort(404)
        return None


@APP.route("/sapmasterdata/master/<asset_id>", methods=["GET"])
# @APP.route("/sapmasterdata/master/$filter=Sernr%20eq%20<serial_number_of_the_aggregate>&?format=json", methods=["GET"])
@AUTH.login_required
def get_sapmasterdata_master(asset_id):
    try:
        if request.method == 'GET':
            if asset_id:
                data = read_json(asset_id, Config.mock_data_source_sapmasterdata_master)
                return jsonify(data), 200
            abort(404)
        return None
    except:
        abort(404)
        return None


@APP.route('/sapbomasbuilt/asbuilt/<assetid>', methods=["GET"])
@AUTH.login_required
def get_sapbomasbuilt_asbuilt(assetid):
    try:
        if request.method == 'GET':
            if assetid:
                data = read_json(assetid, Config.mock_data_source_sapbomasbuilt_asbuilt)
                return jsonify(data), 200
            abort(404)
        return None
    except:
        abort(404)
        return None


@APP.route('/sapbomasbuilt/asmaint/<assetid>/<valid_from>', methods=["GET"])
@AUTH.login_required
def get_sapbomasbuilt_asmaint(assetid, valid_from):
    try:
        if request.method == 'GET':
            if assetid and valid_from == "2018":
                data = read_json(assetid, Config.mock_data_source_sapbomasbuilt_asmaint)
                return jsonify(data), 200
            abort(404)
        return None
    except:
        abort(404)
        return None


@APP.route('/sapequipmenthistory/history/<assetid>', methods=["GET"])
@AUTH.login_required
def get_sapequipmenthistory_asset(assetid):
    try:
        if request.method == 'GET':
            if assetid:
                data = read_json(assetid, Config.mock_data_source_sapequipmenthistory_history)
                return jsonify(data), 200
            abort(404)
        return None
    except:
        abort(404)
        return None


@APP.route('/sapequipmenthistory/documents/<equnr>', methods=["GET"])
@AUTH.login_required
def get_sapequipmenthistory_equnr(equnr):
    try:
        if request.method == 'GET':
            if equnr:
                data = read_json(equnr, Config.mock_data_source_sapequipmenthistory_documents)
                return jsonify(data), 200
            abort(404)
        return None
    except:
        abort(404)
        return None


@APP.route('/sapequipmenthistory/document/<instid>', methods=["GET"])
@AUTH.login_required
def get_sapequipmenthistory_instid(instid):
    try:
        if request.method == 'GET':
            if instid:
                data = read_json(instid, Config.mock_data_source_sapequipmenthistory_document)
                return jsonify(data), 200
            abort(404)
        return None
    except:
        abort(404)
        return None


@APP.route('/sapmasterdata/<assetid>', methods=["GET"])
@AUTH.login_required
def get_sapmasterdata(assetid):
    try:
        if request.method == 'GET':
            if assetid:
                data = read_json(assetid, Config.mock_data_source_sapmasterdata)
                return jsonify(data), 200
            abort(404)
        return None
    except:
        abort(404)
        return None


@APP.route('/sapmaterial/supersession/<materialnumber>', methods=["GET"])
@AUTH.login_required
def get_sapsupersession(materialnumber):
    try:
        if request.method == 'GET':
            if materialnumber:
                data = read_json(materialnumber, Config.mock_data_source_sapmaterial_supersession)
                return jsonify(data), 200
            abort(404)
        return None
    except:
        abort(404)
        return None


@APP.route('/sapmaterial/masterdata/<materialnumber>', methods=["GET"])
@AUTH.login_required
def get_materialmaster(materialnumber):
    try:
        if request.method == 'GET':
            if materialnumber:
                data = read_json(materialnumber, Config.mock_data_source_sapmaterial_masterdata)
                return jsonify(data), 200
            abort(404)
        return None
    except:
        abort(404)
        return None


@APP.route('/sapwarrantyrecall/<assetid>', methods=["GET"])
@AUTH.login_required
def get_sapwarrantyrecall(assetid):
    try:
        if request.method == 'GET':
            if assetid:
                data = read_json(assetid, Config.mock_data_source_sapwarrantyrecall)
                return jsonify(data), 200
            abort(404)
        return None
    except:
        abort(404)
        return None


@APP.route('/talendfirmware/<assetid>', methods=["GET"])
@AUTH.login_required
def get_talendfirmware(assetid):
    try:
        if request.method == 'GET':
            if assetid:
                data = read_json(assetid, Config.mock_data_source_talendfirmware)
                return jsonify(data), 200
            abort(404)
        return None
    except:
        abort(404)
        return None


@APP.route('/talendtimdocument/documents/<assetid>', methods=["GET"])
@AUTH.login_required
def get_talendtimdocument_documents(assetid):
    try:
        if request.method == 'GET':
            if assetid:
                data = read_json(assetid, Config.mock_data_source_talendtimdocument_documents)
                return jsonify(data), 200
            abort(404)
        return None
    except:
        abort(404)


@APP.route('/talendtimdocument/document/<assetid>/<doclabel>/<filename>', methods=["GET"])
@AUTH.login_required
def get_talendtimdocument_document(assetid, doclabel, filename):
    try:
        if request.method == 'GET':
            if assetid and doclabel and filename:
                data = read_json(filename, Config.mock_data_source_talendtimdocument_document)
                return jsonify(data), 200
            abort(404)
        return None
    except:
        abort(404)
        return None


def main():
    APP.run(host='localhost', port=5000, debug=True)


if __name__ == '__main__':
    main()
