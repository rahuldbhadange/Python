# import json
# import numpy as np
from flask import Flask, request, jsonify, redirect, url_for, session, render_template
from flasgger import Swagger
from flasgger.utils import swag_from
from flasgger import LazyString, LazyJSONEncoder
import pymongo
import connexion
# from pprint import pprint

# Create the application instance
app = connexion.App(__name__, specification_dir='./')


Client = pymongo.MongoClient("mongodb://localhost:27017/")
DB = Client.database2019
collection10 = DB["swagger"]
# collection10 = DB["swagger_new"]

# app = Flask(__name__)
# # app.config["DEBUG"] = True
# app.config["SWAGGER"] = {"title": "Swagger Basics", "uiversion": 3}
#
# swagger_config = {
#     "headers": [],
#     "specs": [
#         {
#             "endpoint": "apispec_1",
#             "route": "/apispec_1.json",     # swagger_config
#             "rule_filter": lambda rule: True,  # all in
#             "model_filter": lambda tag: True,  # all in
#         }
#     ],
#     "static_url_path": "/flasgger_static",
#     "static_folder": "static",  # must be set by user
#     "swagger_ui": True,
#     "specs_route": "/swagger/",    # main url
# }
#
# template = dict(
#     swaggerUiPrefix=LazyString(lambda: request.environ.get("HTTP_X_SCRIPT_NAME", ""))
# )
#
# app.json_encoder = LazyJSONEncoder
# swagger = Swagger(app, config=swagger_config, template=template)


@app.route("/")
def index():
    return "<h1>swagger</h1>"


@app.route("/app_get", methods=['GET'])
# @swag_from("get_config.yml")    # swag_from() accepts input 'dict' or 'yml file'
@swag_from("total_config.yaml")
def _view_function():
    _res = DB.swagger.find()
    # for p in DB.swagger.find():
    #     template = {
    #         "name": None,
    #         "location": None,
    #         "phone_no": None,
    #         "pan_no": None
    #     }
    #
    #     template["name"] = str(p["name"])
    #     template["location"] = str(p["location"])
    #     template["phone_no"] = int(p["phone_no"])
    #     template["pan_no"] = int(p["pan_no"])
    #
    #     _res.append(template)
    # res = dict(_res)        # this will not work
    # return jsonify(_res)
    # return jsonify({"hello": "GET"})
    return [_res[key] for key in sorted(_res.keys())]


@app.route("/app_post", methods=['POST'])
# @swag_from("post_config.yml")    # swag_from() accepts the input dict or yml file
@swag_from("total_config.yml")    # swag_from() accepts the input dict or yml file
def _add_function(name, location):
    _Port = None
    # input_json = request.get_json()

    # name = str(input_json["name"])
    # location = str(input_json["location"])
    # _Port = {"name": "Sony", "location": "TN"}
    _Port = {"name": name, "location": location}

    DB.swagger.insert_one(_Port)
    # return jsonify({"hello": "POST"})
    # return jsonify(_Port)
    # return _Port
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
    # # return jsonify({"hello": "POST"})
    # return jsonify(_Port)


# @app.route("/post_2_numbers", methods=["POST"])
# @swag_from("old.yaml")    # swag_from() accepts the input dict or yml file
# def add_numbers():
#     input_json = request.get_json()
#     output = {"sum_of_numbers": 0}
#     try:
#         num1 = int(input_json["x1"])
#         num2 = int(input_json["x2"])
#         res = add_2_numbers(num1, num2)
#         output["sum_of_numbers"] = res
#         # DB.swagger.insert_one(output)
#         # output = {"sum_of_numbers": 0}
#
#         # res1 = res
#     except:
#         res = {"success": False, "message": "Unknown error"}
#     # p = json.dumps(res)
#     return json.dumps(output)
#     # DB.swagger.insert_one(output)


# @app.route("/replace", methods=["PUT"])
# @swag_from("replace_config.yml")    # swag_from() accepts the input dict or yml file
# # @swag_from("swagger_config.yaml")    # swag_from() accepts the input dict or yml file
# def _replace_function():
#     # return "<h1>BYE !!!</h1>"
#     input_json = request.get_json()
#
#     name = str(input_json["name"])
#     new_name = str(input_json["new_name"])
#
#     DB.swagger.replace_one({'name': name}, {'name': new_name})    # replacing existing doc element
#     return jsonify({"hello": "PUT"})
#
#
# @app.route("/update", methods=["PUT"])
# @swag_from("update_config.yml")    # swag_from() accepts the input dict or yml file
# # @swag_from("swagger_config.yaml")    # swag_from() accepts the input dict or yml file
# def _update_function():
#     # return "<h1>BYE !!!</h1>"
#     input_json = request.get_json()
#     phone_no = int(input_json['phone_no'])
#     pan_no = str(input_json['pan_no'])
#     DB.swagger.update_one({'phone_no': phone_no})       # updating existing doc with new field
#     DB.swagger.update_many({'phone_no': phone_no}, {'pan_no': pan_no})  # updating existing doc with new multiple field
#     # return jsonify({"hello": "PUT"})
#
#
# @app.route("/delete", methods=["DELETE"])
# @swag_from("delete_config.yml")    # swag_from() accepts the input dict or yml file
# # @swag_from("swagger_config.yaml")    # swag_from() accepts the input dict or yml file
# def _delete_function():
#     # return "<h1>BYE !!!</h1>"
#     input_json = request.get_json()
#
#     name = str(input_json["name"])
#     DB.swagger.delete_one({'name': name})   # first in collection
#     DB.swagger.delete_many({'name': name})  # all that matches in collection
#     # return jsonify({"hello": "DELETE"})


# @app.route('/home/', methods=['POST'], defaults={'name': 'Default or Anything'})
# @app.route('/home/<string:name>', methods=['POST'])     # request type '<string:name>'
# def home(name):
#     session["name"] = name  # cookies: saving it to session, it remembers the basic stuff like username etc.
#     # location = location
#     return render_template(
#         'home.html', name=name, display=True,
#         my_dict=[{'one': '1', }, {'two': '2'}, {'three': '3'}, {'four': '4'}],
#         my_list=['One', 'Two', 'Three', 'Four'])    # render HTML template or any other specific info

# def add_2_numbers(num1, num2):
#     # output = {"sum_of_numbers": 0}
#     sum_of_2_numbers = num1 + num2
#     # output["sum_of_numbers"] = sum_of_2_numbers
#     # return output
#     return sum_of_2_numbers
#
#
# _dict = {}
#
# def change_2_numbers(num1, num2):
#     output = {"sum_of_numbers": 0}
#     sum_of_2_numbers = num1 + num2
#     output["sum_of_numbers"] = sum_of_2_numbers
#     return output

# @app.route("/post", methods=['POST'])
# @swag_from("old.yaml")    # swag_from() accepts the input dict or yml file
# def get_numbers():
#     # return "<h1>BYE !!!</h1>"
#     input_json = request.get_json()
#     try:
#         num1 = int(input_json["x1"])
#         num2 = int(input_json["x2"])
#         res = add_2_numbers(num1, num2)
#         # _dict[num1] = num2
#     except:
#         res = {"success": False, "message": "Unknown error"}
#     # return jsonify({"hello": "GET"})



# Read the swagger.yml file to configure the endpoints
app.add_api('total_config.yml')


if __name__ == "__main__":
    app.run(debug=True, port=8081)
