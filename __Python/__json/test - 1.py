import json
#
# with open('mock-data.json', mode="r", encoding="utf-8") as f:
#     data = json.load(f)
# print(data, type(data))


endpoint = 'http://defnsv2380.fn2.mtufn.com:8040/services/firmware/version/Talend_Firmware_ASSET_ID'

asset_id = '12364568'


# endpoint = endpoint.replace('Talend_Firmware_ASSET_ID', asset_id)
endpoint = endpoint + "?={}".format(asset_id)
print(endpoint)



# data=json.dumps(rqst_data