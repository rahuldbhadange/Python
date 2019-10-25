import requests
import json
# from flask import request, jsonify
#
# from werkzeug.wrappers import Request, Response

usr = 'talendtimdocument'
pwd = 'talendtimdocument'

print('\nstarting request of talendtimdocument\n')


def response():
    print('in the response function \n')
    resp = requests.get('http://localhost:5000/talendtimdocument-mock-data/view', auth=(usr, pwd))
    print('after request response saved in variable \n')
    print('json response is : \n', resp.json())
    # mock_data = json.load(resp)
    # print(mock_data)
    print('\n the end of __Request.py')
#    return jsonify(mock_data)


response()
