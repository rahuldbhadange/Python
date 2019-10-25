from flask import Flask, request, jsonify, redirect, url_for, make_response  # From module flask import class Flask

# from werkzeug.wrappers import Request, Response


app = Flask(__name__)  # Construct an instance of Flask class for our webapp
app.config["DEBUG"] = True  # Enable reloader and debugger

# Create some test data for our catalog in the form of a list of dictionaries.
sapwarrantyrecall = [
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


# authentication = {"usr": "usr", "pwd": "pwd"}


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return make_response(
        'Could not verify your access level for that URL. You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route('/')
def welcome():
    return 'welcome'


# def authenticate():
#     """Sends a 401 response that enables basic auth"""
#     return make_response(
#         'Could not verify your access level for that URL. You have to login with proper credentials', 401,
#         {'WWW-Authenticate': 'Basic realm="Login Required"'})


# @app.route('/login', methods=['GET'])
# def requires_auth():
#     auth = request.authorization
#     if not auth or not check_auth(auth.username, auth.password):  # no header set
#         return authenticate()
#     else:
#         return "sucessfully login"


@app.route('/login', methods=['GET'])
def requires_auth():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):  # no header set
        return authenticate()
    else:
        return "sucessfully login"


@app.errorhandler(404)
def page_not_found():
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


# @app.route('/')
# def main():
#     return redirect(url_for('hello.html', username='Peter'))
#         # Also pass an optional URL variable


# @app.route('/hello/<username>')  # URL with a variable
# def hello_username(username):    # The function shall take the URL variable as parameter
#     return 'Hello, {}'.format(username)
#
#
# @app.route('/hello/<int:userid>')  # Variable with type filter. Accept only int
# def hello_userid(userid):          # The function shall take the URL variable as parameter
#     return 'Hello, your ID is: {:d}'.format(userid)


# @app.route('/', methods=['GET'])  # URL '/' to be handled by main() route handler (or view function)
# def home():
#     return '''<h1>Distant Reading Archive</h1>
# <p>A prototype API for distant reading of science fiction novels.</p>'''

#
# @app.route('/hello', methods=['GET'])  # URL '/' to be handled by main() route handler (or view function)
# def hello():
#     return 'hello'


@app.route('/sapwarrantyrecall/all', methods=['GET'])
def api_all():
    return jsonify(sapwarrantyrecall)


@app.route('/sapwarrantyrecall', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in th  e browser.
    if 'asset_id' in request.args:
        id = int(request.args['asset_id'])
        # if "usr" in request.args:
        #     usr = str(request.args['usr'])
        #     if "pwd" in request.args:
        #         pwd = str(request.args['pwd'])

    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    # for auth in authentication:
    #     if auth['usr'] == usr and auth['pwd'] == pwd:
    for sap in sapwarrantyrecall:
        if sap['asset_id'] == id:
            results.append(sap)
    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)


if __name__ == '__main__':  # Script executed directly?
    app.run()  # Launch built-in web server and run this Flask webapp


# if __name__ == '__main__':  # Script executed directly (instead of via import)?
#     from werkzeug.serving import run_simple
#
#     run_simple('localhost', 5000, app)  # Launch built-in web server and run this Flask webapp
