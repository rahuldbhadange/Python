import json

from flask import Flask, request, jsonify, redirect, url_for, session, render_template
import pymongo
import connexion


# Create the application instance
app = connexion.App(__name__, specification_dir='./')


Client = pymongo.MongoClient("mongodb://localhost:27017/")
DB = Client.database2019
collection10 = DB["swagger"]


app.app.js
app.add_api()
app.add_error_handler()

# Create a URL route in our application for "/"
@app.route('/app')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/

    :return:        the rendered template 'home.html'
    """
    return render_template('homie.html')


# def _add_function(name, location):
def _add_function():
    # if request.method == "POST":
    #     return render_template('form.html')
    # else:
    #     name = 'edfghj'
    #     location = 'rtghfgh'
    #     # return 'Hello, {} !! Welcome to {} city. You have successfully submitted form !!'.format(name, location)
    #     return redirect(url_for('home', name=name, location=location))


    # _Port = None
    # input_json = request.get_json()
    #
    # name = str(input_json["name"])
    # location = str(input_json["location"])
    # # _Port = {"name": "Sony", "location": "TN"}
    # _Port = {"name": name, "location": location}
    #
    # DB.swagger.insert_one(_Port)
    # name = 'edfghj'
    # location = 'rtghfgh'
    # return jsonify({"hello": "POST"})
    # return jsonify(_Port)
    # return jsonify({"name": name, "location": location})    # return _Port
    # p = {"name": name, "location": location}
    # DB.swagger.insert_one(p)
    # print(p)
    # return json.dumps(_Port)

    # try:
    #     # name = request.args.get('name')  # important: we can get the args from input
    #     # location = request.args.get('location')
    #     name = str(input_json["name"])
    #     location = str(input_json["location"])
    #     # name = "Rahul"
    #     # location = "Bengaluru"
    #     try:
    #         _Port = {"name": name, "location": location}
    #         DB.swagger.insert_one(_Port)
    #     except Exception as EX:
    #         print("Error is: ", EX)
    # except:
    #     res = {"success": False, "message": "Unknown error"}
    # # return redirect(url_for('home', name=name, location=location))
    return jsonify({"hello": "POST"})
    # return jsonify(_Port)


def _view_function():
    # return "<h1>BYE !!!</h1>"
    _res = []
    # p = DB.swagger.find_one({"name": "Raj"})
    for p in DB.swagger.find():
        template = {
            "_id": None,
            "name": None,
            "location": None,
            # "phone_no": None,
            # "pan_no": None
        }
        template["_id"] = str(p['_id'])
        template["name"] = str(p["name"])
        template["location"] = str(p["location"])
        # template["phone_no"] = int(p["phone_no"])
        # template["pan_no"] = int(p["pan_no"])

        _res.append(template)
    # return jsonify(_res)
    return _res
    # return render_template('form.html')


# Read the swagger.yml file to configure the endpoints
app.add_api('new.yml')


if __name__ == "__main__":
    app.run(debug=True, port=8080, host='localhost')
