from flask import Flask, request, jsonify, redirect, url_for, make_response, abort  # From module flask import class Flask
from werkzeug.serving import run_simple
#from werkzeug.wrappers import Request, Response
import json
import http.client


app = Flask(__name__)  # Construct an instance of Flask class for our webapp
app.config["DEBUG"] = True  # Enable reloader and debugger


def validate_auth():
    auth = request.authorization
    if not auth:  # no header set
        abort(401)
    # user = UserModel.query.filter_by(username=auth.username).first()
    # if user is None or user.password != auth.password:
    #     abort(401)


def check_auth(username, password):
    """This function is called to check if a username, password combination is valid."""
    return username == 'usr' and password == 'pwd'


@app.route('/sapwarrantyrecall-mock-data', methods=['GET'])
def api_all():
    auth = request.authorization
    if not auth:  # no header set
        abort(401)
#    validate_auth()
    else:
        input_file = open('sapwarrantyrecall-mock-data.json', 'r')
        mock_data = json.load(input_file)
    # results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    # for auth in authentication:
    # for sap in mock_data:
    #     if sap['asset_id'] == asset_id:
    #         results.append(sap)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    # return jsonify(results)
    return jsonify(mock_data)


@app.route('/talendtimdocument-mock-data&&<username>&<password>', methods=['GET'])
def talendtimdocument_auth(username, password):
    if not check_auth(username, password):
        """Sends a 401 response that enables basic auth"""
        return make_response(
            'Could not verify your access level for that URL. You have to login with proper credentials', 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'})
    else:
        input_file = open('talendtimdocument-mock-data.json', 'r')
        mock_data = json.load(input_file)
        # Use the jsonify function from Flask to convert our list of
        # Python dictionaries to the JSON format.
    return jsonify(mock_data)


if __name__ == '__main__':  # Script executed directly (instead of via import)?
    run_simple('localhost', 5000, app)  # Launch built-in web server and run this Flask webapp