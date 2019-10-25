from flask import Flask, request, jsonify, redirect, url_for, make_response  # From module flask import class Flask
from werkzeug.serving import run_simple
#from werkzeug.wrappers import Request, Response
import json

app = Flask(__name__)  # Construct an instance of Flask class for our webapp
app.config["DEBUG"] = True  # Enable reloader and debugger


sapwarrantyrecall_mock_data =[
    {'asset_id': 5242454668,
     "Pnguid": "AFBWiyhYHtiE5aq+SeSqiw==",
     "Pncnt": "00000001",
     "HPntext": "2018.02.16.0001",
     "Clmno": "000440000120",
     "Clmty": "YCIF",
     "Refdt": "\/Date(1514764800000)\/",
     "Refno": "2018.02.16.0001",
     "Sernr": "",
     "Equnr": "000000000010000018",
     "Parnr": "",
     "Astate": "YC20",
     "Abdes": "Active",
     "YywtyState": "",
     "YycifPrio": "M",
     "YycifPriotxt": "Modifikation",
     "Yyroopen": "0000-00-00",
     "Yyroclosed": "0000-00-00",
     "YydueDate": "2018-12-31",
     "Yysystfir": "",
     "Yyclmtype": "",
     "Yyclmtypetxt": "",
     "Yyrepcountry": "",
     "DocLink": "HTTP://WWW.PRORATA-NOW.COM"},
    {'asset_id': 5242454669,
     "Pnguid": "AFBWiyhYHtiE5ie9Vxcqiw==",
     "Pncnt": "00000001",
     "HPntext": "2018.02.16.0002",
     "Clmno": "000440000121",
     "Clmty": "YCIF",
     "Refdt": "\/Date(1514764800000)\/",
     "Refno": "2018.02.16.0002",
     "Sernr": "",
     "Equnr": "000000000010000018",
     "Parnr": "",
     "Astate": "YC20",
     "Abdes": "Active",
     "YywtyState": "",
     "YycifPrio": "M",
     "YycifPriotxt": "Modifikation",
     "Yyroopen": "0000-00-00",
     "Yyroclosed": "0000-00-00",
     "YydueDate": "2018-12-31",
     "Yysystfir": "",
     "Yyclmtype": "",
     "Yyclmtypetxt": "",
     "Yyrepcountry": "",
     "DocLink": "http://www.google.de"}
]

def check_auth(username, password):
    """This function is called to check if a username, password combination is valid."""
    return username == 'usr' and password == 'pwd'


@app.route('/sapwarrantyrecall/<int:asset_id>', methods=['GET'])
def api_all(asset_id):
    input_file = open('mock-data.json', 'r')
    mock_data = json.load(input_file)
    # print(mock_data)
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    # for auth in authentication:
    #     if auth['usr'] == usr and auth['pwd'] == pwd:
    for sap in mock_data:
        if sap['d']['results']['asset_id'] == asset_id:
            results.append(sap)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)
    #return jsonify(mock_data)


@app.route('/sapwarrantyrecall/<int:asset_id>&<username>&<password>', methods=['GET'])  # Variable with type filter. Accept only int
def hello_test(asset_id, username, password):          # The function shall take the URL variable as parameter
    if not check_auth(username, password):
        """Sends a 401 response that enables basic auth"""
        return make_response(
            'Could not verify your access level for that URL. You have to login with proper credentials', 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'})
    else:
        results = []
        # input_file = open('mock-data.json', 'r')
        # input = json.load(input_file)
        for data in sapwarrantyrecall_mock_data:
            if data['asset_id'] == asset_id:     #  if sap['d']['results']['asset_id'] == asset_id:
                results.append(data)
        # Use the jsonify function from Flask to convert our list of
        # Python dictionaries to the JSON format.
        return jsonify(results)


if __name__ == '__main__':  # Script executed directly (instead of via import)?
    run_simple('localhost', 5000, app)  # Launch built-in web server and run this Flask webapp
