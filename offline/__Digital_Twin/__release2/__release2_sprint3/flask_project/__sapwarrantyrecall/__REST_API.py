from flask import Flask, request, jsonify, abort
from werkzeug.serving import run_simple
import json


app = Flask(__name__)  # Construct an instance of Flask class for our webapp
app.config["DEBUG"] = True  # Enable reloader and debugger


@app.route('/', methods=['GET'])
def api_sapwarrantyrecall_hello():
    return 'hello sapwarrantyrecall'


@app.route('/sapwarrantyrecall-mock-data/view', methods=['GET'])
def api_sapwarrantyrecall_auth():
    print("in api all")
    auth = request.authorization
    print('after auth')
    if not auth:  # no header set
        # return 'Bad Request', 401
        abort(401)
    else:
        # return 'good request'
        input_file = open('sapwarrantyrecall-mock-data.json', 'r')
        mock_data = json.load(input_file)
    # results = []
    # return jsonify(results)
    return jsonify(mock_data)


@app.route('/sapwarrantyrecall-mock-data', methods=['GET'])
def api_sapwarrantyrecall_all():
    input_file = open('sapwarrantyrecall-mock-data.json', 'r')
    mock_data = json.load(input_file)
    # results = []
    # return jsonify(results)
    return jsonify(mock_data)


if __name__ == '__main__':  # Script executed directly (instead of via import)?
    run_simple('localhost', 5000, app, use_debugger=True)  # Launch built-in web server and run this Flask webapp
