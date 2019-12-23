from urllib.request import localhost

from flask import Flask, jsonify, render_template, request, session, url_for, redirect
from flask_httpauth import HTTPBasicAuth
from pymongo import MongoClient
import requests
import json
# from requests_html import HTMLSession
# session = HTMLSession()
import requests as req
from pymongo.message import (_INSERT, _UPDATE, _DELETE,
                             _do_batched_insert,
                             _do_bulk_write_command,
                             _randint,
                             _BulkWriteContext)

app = Flask(__name__)
AUTH = HTTPBasicAuth()

app.config["DEBUG"] = True

Client = MongoClient('mongodb://localhost:27017/')  # "mongodb://localhost:27017/"
_database = Client.personal
_collection = _database['personal']
_db_obj = _database.personal

connection_string = ""
database = ""

# CRUD

"""@AUTH.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return Config.USER_DATA.get(username) == password"""


@app.route("/data$filter=Sernr%20eq%20'4711-0006'&?format=json", methods=["GET", "POST"] )
def _filter(Sernr):
    return jsonify({"Rahul": "Raj", "Sernr": Sernr})
    # return "doing something with {} args".format(Sernr)


@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def _base():
    if request.method == "GET":
        return render_template('base.html')

    elif request.method == "GET":
        return '<h2>GET</h2>'

    elif request.method == 'DELETE':
        return "<h2>DELETE</h2>"

    elif request.method == "PUT":
        return "<h2>PUT</h2>"
    # return """<h1>Distant Reading Archive</h1>
    # <p>This site is a prototype API for distant reading of science fiction novels.</p>"""


@app.route('/home', methods=['GET', 'POST', 'PUT', 'DELETE'])
def _home():
    if request.method == "POST":
        return render_template('home.html')

    elif request.method == "GET":
        return '<h2>GET</h2>'

    elif request.method == 'DELETE':
        return "<h2>DELETE</h2>"

    elif request.method == "PUT":
        return "<h2>PUT</h2>"


@app.route('/create', methods=['GET', 'POST', 'PUT', 'DELETE'])
def _create():
    if request.method == "POST":
        _data = []

        data = {"Name": request.form['name'], "Location": request.form['location'],
                "Username": request.form['username'], "E-mail": request.form['email'],
                "Password": request.form['password']}

        _data.append(data)
        _database.personal.insert_many(_data)

        return 'Hello {}. You have successfully submitted the form.'.format(request.form['name'])

    elif request.method == "GET":
        return '<h2>GET</h2>'

    elif request.method == 'DELETE':
        return "<h2>DELETE</h2>"

    elif request.method == "PUT":
        return "<h2>PUT</h2>"


@app.route('/home/create', methods=['GET', 'POST', 'PUT', 'DELETE'])
def __create():

    if request.method == "POST":
        return render_template('create.html')

    elif request.method == "GET":
        return '<h2>GET</h2>'

    elif request.method == 'DELETE':
        return "<h2>DELETE</h2>"

    elif request.method == "PUT":
        return "<h2>PUT</h2>"


@app.route('/home/read', methods=['GET', 'POST', 'PUT', 'DELETE'])
def __read():

    if request.method == "POST":
        return render_template('read.html')
    # name = request.form['name']
    # location = request.form['location']
    # return 'Hello, {} !! Welcome to {} city. You have successfully submitted form !!'.format(name, location)
    # return redirect(url_for('_read', name=name))

    elif request.method == "GET":
        name = input('name ??')

    elif request.method == 'DELETE':
        return "<h2>DELETE</h2>"

    elif request.method == "PUT":
        return "<h2>PUT</h2>"


@app.route('/read', methods=['GET', 'POST', 'PUT', 'DELETE'])
def _read():
    # name = session['name']    -   need to try this
    if request.method == "POST":
        try:
            if 'name' in request.form:
                name = str(request.form['name'])
                _res = []

                _person = _db_obj.find({'Name': name})
                # _res.append(result)
                if _person:
                    for person in _person:
                        _data = {"Name": person["Name"], "Location": person["Location"],
                                 "Username": person["Username"], "E-mail": person["E-mail"],
                                 "Password": person["Password"]}

                        _res.append(_data)
                else:
                    return "<h2>No Data Found</h2>"

                if _res:
                    return jsonify(_res)
            else:
                return "Please Enter the Name"
        except Exception as Ex:
            return "<h2>error is: {}</h2>".format(Ex)
    elif request.method == "GET":
        return '<h2>GET</h2>'

    elif request.method == 'DELETE':
        return "<h2>DELETE</h2>"

    elif request.method == "PUT":
        return "<h2>PUT</h2>"


@app.route('/login', methods=['GET', 'POST', 'PUT', 'DELETE'])
def login():
    if request.method == "POST":
        if 'name' in request.form:
            _res = []
            # if _name == person["Name"]:
            _name = str(request.form['name'])
            _password = str(request.form['password'])
            _person = _db_obj.find({"Name": _name})
            if _person:
                for person in _person:
                    _data = {"Name": person["Name"], "Location": person["Location"],
                             "Username": person["Username"], "E-mail": person["E-mail"],
                             "Password": person["Password"]}

                    if str(person["Name"]) == _name and str(person["Password"]) == _password:
                        _res.append(_data)
            else:
                return "nnn"
            return jsonify(_res)
        # else:
        #     return 'Not a Valid Name. Please Enter Valid Name.'
    elif request.method == "GET":
        return '<h2>GET</h2>'

    elif request.method == 'DELETE':
        return "<h2>DELETE</h2>"

    elif request.method == "PUT":
        return "<h2>PUT</h2>"


@app.route('/name_update')
def __update():
    _name = request.args.get('name')
    _password = request.args.get('password')
    return '__update : {} {}'.format(_name, _password)


@app.route('/home/update', methods=['GET', 'POST', 'PUT', 'DELETE'])
def update():

    if request.method == "POST":
        return render_template('login.html')
        
    elif request.method == "GET":
        return '<h2>GET</h2>'

    elif request.method == 'DELETE':
        return "<h2>DELETE</h2>"

    elif request.method == "PUT":
        return "<h2>PUT</h2>"


@app.route('/update', methods=['GET', 'POST', 'PUT', 'DELETE'])
def _update():
    # return 'What you want to update'
    if request.method == "POST":
        _name = request.form['name']
        _password = request.form['password']

        person = _db_obj.find({"Name": _name})

        if person.p["Name"] == _name and person.p["Password"] == _password:
            return render_template('form.html')
        # return url_for('__update', name=name, password=password)      - need to try
        # return '__update : {} {}'.format(_name, _password)
        else:
            return "Bad Request"

    elif request.method == "GET":
            return '<h2>GET</h2>'

    elif request.method == 'DELETE':
        return "<h2>DELETE</h2>"

    elif request.method == "PUT":
        return "<h2>PUT</h2>"

    # return '<h2>updated.  {}</h2>'.format(name)
    # return render_template('update.html')


@app.route('/home/delete_new', methods=['GET', 'POST', 'PUT', 'DELETE'])
def __delete():

    if request.method == "POST":
        return render_template('delete_new.html')

    elif request.method == "GET":
        return '<h2>GET</h2>'

    elif request.method == 'DELETE':
        return "<h2>DELETE</h2>"

    elif request.method == "PUT":
        return "<h2>PUT</h2>"


@app.route('/home/delete', methods=['GET', 'POST', 'DELETE', 'PUT'])
def _delete():

    if request.method == 'POST':
        _name = request.form['name']

        try:
            list_of_name = []
            # _list_of_name = jsonify(list_of_name)

            _person = _database['personal'].find({'Name': _name})
            if _person:
                _db_obj.delete_one({'Name': _name})

                for person in _database['personal'].find():

                    _data = {"Name": person["Name"], "Location": person["Location"]}

                    list_of_name.append(_data)

                return "<h3>Your Name has been successfully deleted from database.<h3>\n" + \
                       "<h4>\n Current data is {}\n</h4>".format(list_of_name)

            else:
                return "<h2>This {} does not exist in Database. Please Enter Valid Name.</h2>".format(_name)

        except Exception as Ex:
            return "<h2>We are not able to delete your 'Name' from database. {}</h2>".format(Ex)

    elif request.method == "GET":
        return '<h2>GET</h2>'

    elif request.method == 'DELETE':
        return "<h2>DELETE</h2>"

    elif request.method == "PUT":
        return "<h2>PUT</h2>"



































































































@app.route('/thank', methods=['GET', 'POST', 'PUT', 'DELETE'])
# def _thank(name, location, username, email, password):
def _thank():
    # session["name"] = name        - need to try this

    if request.method == 'GET':
        return 'hello'
        # return render_template('form.html')
    elif request.method == 'POST':
        name = request.form['name']
        location = request.form['location:']
        return jsonify({'Name': name, 'Location': location})
        # return 'hi'

    # endpoint = 'http://127.0.0.1:5000/home/create'
    # endpoint = 'http://127.0.0.1:5000/thank'
    # resp = requests.get(endpoint, auth=None, verify=False, timeout=None)
    # if resp.ok:
    #     try:
    #         _data = []
    # name = resp['Name']
    # location = resp['Location']
    # username = resp['Username']
    # email = resp['E-mail']
    # password = resp['Password']
    #
    # data = {"Name": name,
    #         "Location": location,
    #         "Username": username,
    #         "E-mail": email,
    #         "Password": password}
    # _data.append(data)

    # results = resp.json()
    # data = {"Name": '',
    #          "Location": '',
    #          "Username": '',
    #          "E-mail": '',
    #          "Password": ''}

    # for person in results:
    # _data["Name"] = results["Name"]
    # _data["Location"] = results["Location"]
    # _data["Username"] = results["Username"]
    # _data["E-mail"] = results["E-mail"]
    # _data["Password"] = results["Password"]
    #
    # _data.append(data)

    #         data = {"Name": 'Badri',
    #                 "Location": 'location',
    #                 "Username": 'username',
    #                 "E-mail": 'email',
    #                 "Password": 'password'}
    #         _data.append(data)
    #
    #         try:
    #             _database.personal.insert_many(_data)
    #             return '<h2>Your response has been recorded in database</h2>'
    #         except Exception as Ex:
    #             return '<h3>Unable to record your response: {}</h3>'.format(Ex)
    #     except Exception as Ex:
    #         return '<h3>Something went wrong: {}</h3>'.format(Ex)
    # else:
    #     return 'resp: {}'.format(resp)

    # input_json = request.get_json()

    # name = str(input_json["Name"])
    # _data = []
    # name = request.args.get('Name')
    # location = request.args.get('Location')
    # username = request.args.get('Username')
    # email = request.args.get('E-mail')
    # password = request.args.get('Password')

    # data = {"Name": name,
    #          "Location": location,
    #          "Username": username,
    #          "E-mail": email,
    #          "Password": password}
    # _data.append(data)

    # approch: 3

    # r = session.get('http://127.0.0.1:5000/home/create')
    # r = session.get('http://127.0.0.1:5000/thank')
    # print("r.html.links: ", r.html.links)
    # print("r.html.absolute_links: ", r.html.absolute_links)
    # about = r.html.find('r.html.absolute_links', first=True)
    # print(about.text)
    # print(about.find('a'))
    # print(about.attrs)
    # print(about.html)

    # resp = req.get("http://localhost/home/create")
    # resp = req.get("http://127.0.0.1:5000/thank")
    # print(resp.text)
    # return '<h2>{}</h2>'.format(resp.text)
    # return '<h2>Your response has been recorded.</h2>'


if __name__ == '__main__':
    app.run(port=8080)
