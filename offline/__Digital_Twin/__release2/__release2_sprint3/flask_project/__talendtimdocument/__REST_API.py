from flask import Flask, request, jsonify, abort
from werkzeug.serving import run_simple
import json


app = Flask(__name__)  # Construct an instance of Flask class for our webapp
app.config["DEBUG"] = True  # Enable reloader and debugger


@app.route('/', methods=['GET'])
def api_talendtimdocument_hello():
    return 'hello talendtimdocument'


@app.route('/talendtimdocument-mock-data/view', methods=['GET'])
def api_talendtimdocument_auth():
    print("\nin api_talendtimdocument_auth \n")
    auth = request.authorization
    print('after auth = request.authorization \n')
    if not auth:  # no header set
        print('Bad_Request', 401)
        abort(401)
    else:
        print('\n good request')
        input_file = open('talendtimdocument-mock-data.json', 'r')
        print('\n reading json file, fetched data from it and saved data into variable')
        mock_data = json.load(input_file)
        print('\n json data from variable loading into another variable to return json response ')
    # results = []
    # return jsonify(results)
    return jsonify(mock_data)


@app.route('/talendtimdocument-mock-data', methods=['GET'])
def api_talendtimdocument_all():
    input_file = open('talendtimdocument-mock-data.json', 'r')
    mock_data = json.load(input_file)
    # results = []
    # return jsonify(results)
    return jsonify(mock_data)


if __name__ == '__main__':  # Script executed directly (instead of via import)?
    run_simple('localhost', 5000, app, use_debugger=True)  # Launch built-in web server and run this Flask webapp
