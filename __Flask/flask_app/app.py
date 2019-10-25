from flask import Flask, jsonify, request, redirect, url_for, session, render_template, g
import sqlite3
# import json

app = Flask(__name__)   # create the application instance
app.config.from_object(__name__)    # load config from this file , app.py

app.config["DEBUG"] = True      # Important to remember (Test=True/Production=False)
app.config["SECRET_KEY"] = 'this_is_a_secret'
# data1 = 'data/data.json'


def connect_db():
    """Connects to the specific database."""
    _sql = sqlite3.connect(app.config['DATABASE'])
    _sql.row_factory = sqlite3.Row
    return _sql


@app.route('/')
def index():
    session.pop('name', None)   # deleting session parameter
    return '<h1>Hello World !!!</h1>'


@app.route('/<name>')
def name(name):
    # if 'panda' == name:
    return '<h1>Hello, {} !!</h1>'.format(name)
    # return render_template('Penguins.jpg')


@app.route('/home/', methods=['POST', 'GET'], defaults={'name': 'Default or Anything'}) # We can provide default response, if nothing has mentioned or not acceptable input provided
# @app.route('/home/<name>', methods=['POST', 'GET'])       # request methods = ["GET", "POST"]
# @app.route('/home/<int:name>', methods=['POST', 'GET'])     # request type '<int:name>'
@app.route('/home/<string:name>', methods=['POST', 'GET'])     # request type '<string:name>'
def home(name):
    session["name"] = name  # cookies: saving it to session, it remembers the basic stuff like username etc.
    # location = location
    return render_template(
        'home.html', name=name, display=True,
        my_dict=[{'one': '1', }, {'two': '2'}, {'three': '3'}, {'four': '4'}],
        my_list=['One', 'Two', 'Three', 'Four'])    # render HTML template or any other specific info
    # return '<h1>Hello {}, You are on the home page!</h1>'.format(name)


@app.route('/json', methods=['POST', 'GET'])
def json():
    my_list = [1, 2, 3, 4]
    name = session['name']  # using cookies/session parameter
    # if 'name' in session:
    #     name = session['name']    # logic to show session active or not
    # else:
    #     name = "Not in session"
    return jsonify({'key': 'value', 'key1': [1, 2, 3, 4], 'name': name})  # throwing the session name


@app.route('/query')
def query():
    _name = request.args.get('name')     # we can get the args
    location = request.args.get('location')     #
    return '<h1>Hello, {} !! Welcome to {} city. You are on the query page!</h1>'.format(_name, location)
    # return 'hello'


@app.route('/theform', methods=["GET", "POST"])
# @app.route('/theform')
def theform():
    if request.method == "GET":
        return render_template('form.html')
    else:
        name = request.form['name']
        location = request.form['location']
        # return 'Hello, {} !! Welcome to {} city. You have successfully submitted form !!'.format(name, location)
        return redirect(url_for('home', name=name, location=location))


# @app.route('/process', methods=["POST"])
# def process():
#     name = request.form['name']
#     location = request.form['location']
#     return '<h1>Hello, {} !! Welcome to {} city.
#     You have successfully submitted the form !!</h1>'.format(name, location)


@app.route('/processjson', methods=["POST"])
def jsondata():

    data = request.get_json()   # crating object

    name = data["Name"]
    location = data["Location"]
    randomlist = data["randomlist"]

    return jsonify({"Name": name, "Location": location, "Randomkeyinlist": randomlist[1]})





import pymongo
pymongo.MongoClient(host="", port="", )



























if __name__ == '__main__':
    app.run()

"""@app.route('/theform', methods=["GET","POST"])
def theform():
    return '''<form method="POST">
                <input type = "text" name="name">
                <input type = "text" name="location">
                <input type = "int" name="mobile no">
                <input type = "submit" value="Sign In" method="POST" action="/json">
                <input type = "submit" value="Sign Up" method="POST" action="/query">
            </form>"""

# <input type = "int" name="mobile no">  mobile_no = request.form['mobile no']
