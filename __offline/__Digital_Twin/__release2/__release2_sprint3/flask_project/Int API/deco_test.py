from flask import Flask, request, jsonify, abort, Response
from werkzeug.serving import run_simple
import json
from functools import wraps
# from . import settings


app = Flask(__name__)  # Construct an instance of Flask class for our webapp
app.config["DEBUG"] = True  # Enable reloader and debugger
app.config.from_object('settings')


@app.route('/', methods=['GET'])
def api_talendtimdocument_hello():
    return 'Hello, talendtimdocument !'


def valid_credentials(username, password):
    print('\nchecking valid_credentials')
    # return username == 'talendtimdocument' and password == 'talendtimdocument'
    return username == app.config['USER'] and password == app.config['PASS']
    # return username == settings.config.USER and password == settings.config.PASS


def __require_auth(__talendtimdocument, *args, **kwargs):
    print("\nchecking api_talendtimdocument_auth \n")

    def __inside_fun(*args, **kwargs):
        auth = request.authorization
        if not auth.username or not auth.password or not valid_credentials(auth.username, auth.password):
            print('not valid_credentials')
            return Response('Login!', 401, {'WWW-Authenticate': 'Basic realm="Login!"'})
        print('valid_credentials \n')
        __talendtimdocument()
    return __inside_fun


    # if not auth:  # no header set
    #     print('Bad_Request', 401)
    #     abort(401)
    # else:
    # print('\n good request')
    # input_file = open('talendtimdocument-mock-data.json', 'r')
    # print('\n reading json file, fetched data from it and saved data into variable')
    # mock_data = json.load(input_file)
    # print('\n json data from variable loading into another variable to return json response ')
    # # results = []
    # # return jsonify(results)
    # return jsonify(mock_data)


@app.route('/talendtimdocument-mock-data/view', methods=['GET'])
def __talendtimdocument():
    input_file = open('talendtimdocument-mock-data.json', 'r')
    mock_data = json.load(input_file)
    # results = []
    # return jsonify(results)
    return jsonify(mock_data)


print('object calling')
talendtimdocument = __require_auth(__talendtimdocument)
talendtimdocument()


if __name__ == '__main__':  # Script executed directly (instead of via import)?
    run_simple('localhost', 5000, app)  # Launch built-in web server and run this Flask webapp
