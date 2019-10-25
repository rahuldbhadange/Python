import json

from flask import Flask, request, jsonify, redirect, url_for, session, render_template
import pymongo
import connexion

APP = Flask(__name__)   # create the application instance
APP.config.from_object(__name__)    # load config from this file , app.py


# Create the application instance
app = connexion.App(__name__, specification_dir='./')


Client = pymongo.MongoClient("mongodb://localhost:27017/")
DB = Client.database2019
collection10 = DB["swagger"]


# @app.route('/home', methods=["GET"])
def swagger():
    return render_template('form.html')

# CRUD


# Create a URL route in our application for "/"
# @app.route('/swagger')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/

    :return:        the rendered template 'home.html'
    """
    # return render_template('form.html')
    if request.method == "GET":
        return render_template('form.html')
        # return """<form method="POST" action="/home">
        #                 Name: <input type = "text" name="name" autocomplete="on">
        #                 Location: <input type = "text" name="location" autocomplete="on">
        #                 E-mail: <input type = "email" name="email" autocomplete="on">
        #                 <input type = "submit" value="Submit">
        #         </form>"""
    else:
        # name = request.form['name']
        # location = request.form['location']
        # return 'Hello, {} !! Welcome to {} city. You have successfully submitted form !!'.format(name, location)
        # return redirect(url_for('home', name=name, location=location))
        return jsonify({"hello": "POST"})


# def _add_function(name, location):
# @app.route('/swagger/home', methods=["GET", "POST"])
def _create():
    # return jsonify({"hello": "POST"})
    # return jsonify({"_name_function": name, "_location_function": location})
    if request.method == 'POST':
        return jsonify({"hello": "POST"})
        # _Port = None
        # input_json = request.get_json()
        #
        # name = str(input_json["name"])
        # location = str(input_json["location"])
        # _Port = {"name": name, "location": location}
        # DB.swagger.insert_one(_Port)
    else:
        try:
            # name = request.args.get('name')  # important: we can get the args from input
            # location = request.args.get('location')
            # name = str(input_json["name"])
            # location = str(input_json["location"])
            name = "Roger"
            location = "New York"
            try:
                _Port = {"name": name, "location": location}
                DB.swagger.insert_one(_Port)
            except Exception as EX:
                print("Error is: ", EX)
        except:
            res = {"success": False, "message": "Unknown error"}
        # return redirect(url_for('home', name=name, location=location))
        # return jsonify({"hello": "_create"})
        # return jsonify(_Port)


def test():
    _create()


def _read_app(home):
    return render_template('home.html', home=home)

    # return jsonify({"home": home})
    # return 'Hello, {} !!'.format(home)
    # return redirect(url_for('swagger'))


def _read():
    # return "<h1>BYE !!!</h1>"
    _res = []
    # p = DB.swagger.find_one({"name": "Raj"})
    # db.inventory.find( { $and: [ { price: { $ne: 1.99 } }, { price: { $exists: true } } ] } )
    # _cond = DB.collection2019.find({$and:[{"status": "B"},{"Name":  "Mohan"}}]})
    _cond = DB.collection2019.find()
    # _cond = json.loads(_cond)
    # for p in DB.collection2019.find($and: [{"name": "Rakesh"} , {"status": "B"}]):
    for p in _cond:
        template = {
            "_id": None,
            "name": "",
            "age": "",
            "type": "",
            "status": "",
            # "location": "",
            # "phone_no": None,
            # "pan_no": None
        }
        template["_id"] = str(p['_id'])
        template["name"] = str(p["name"])
        template["age"] = str(p["age"])
        template["type"] = str(p["type"])
        template["status"] = str(p["status"])
        # template["location"] = str(p["location"])
        # template["phone_no"] = int(p["phone_no"])
        # template["pan_no"] = int(p["pan_no"])

        _res.append(template)
    # return jsonify(_res)
    return _res
    # return render_template('form.html')
    # return jsonify({"hello": "_read"})


# def _update_function(name):
def _new_update():
    return jsonify({"hello": "_new_update"})
    # return jsonify({"_update_function": name})


# def _update_function(name):
def _old_update(mobile_no, pan_no):
# def _old_update():
#     input_json = request.get_json()
#     mobile_no = input_json["mobile_no"]
#     pan_no = input_json["pan_no"]
    mobile_no = json.loads(mobile_no)
    pan_no = json.loads(pan_no)

    # return jsonify({"hello": "_old_update"})
    return jsonify({"mobile_no": mobile_no, "pan_no": pan_no})


# def _delete_function(name):
def _delete():
    if 'id' in request.args:
        id = int(request.args['id'])
        return jsonify(id)
    else:
        return "Error: No id field provided. Please specify an id."
    return jsonify({"hello": "_delete"})
    # return jsonify({"_delete_function": name})


@APP.route('/swagger/get', methods=["GET", "POST"])
# @app.route('/theform')
def theform():
    if request.method == "GET":
        return render_template('form.html')
        # return jsonify({"hello": "GET"})
    else:
        name = request.form['name']
        location = request.form['location']
        # return 'Hello, {} !! Welcome to {} city. You have successfully submitted form !!'.format(name, location)
        return redirect(url_for('home', name=name, location=location))


# Read the swagger.yml file to configure the endpoints
app.add_api('request_app.yml')


if __name__ == "__main__":
    app.run(debug=True, port=8080, host='localhost')
