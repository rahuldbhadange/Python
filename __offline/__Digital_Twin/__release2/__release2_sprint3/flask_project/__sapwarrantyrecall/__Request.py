import requests
from flask import request, jsonify
import json
from werkzeug.wrappers import Request, Response

usr = 'sapwarrantyrecall'
pwd = 'sapwarrantyrecall'

print('\nstarting sapwarrantyrecall request\n')


def response():
    print('in the response function \n')
    resp = requests.get('http://localhost:5000/sapwarrantyrecall-mock-data/view', auth=(usr, pwd))
    print('after request response saved in variable \n')
    print('json response is : \n', resp.json())
    # mock_data = json.load(resp)
    # print(mock_data)
    print('\n the end of __Request.py')
#    return jsonify(mock_data)


response()
