import sys

inputString = """([{{
    "_id" : ObjectId("5d108812b6bc8d3280d082b1"),
    "asset_id" : "1000021",
    "Source" : "sapwarrantyrecall",
    "Ts" : "2019-06-24T08:21:37.596035+00:00",
    "Seq" : 838,
    "source" : "sapwarrantyrecall",
    "offset" : 838,
    "_clmno" : "000440000120",
    "AssetType" : "AGG",
    "Type" : "K I F",
    "Details" : [ 
        {
            "EventName" : "Name of Modification",
            "EventValue" : "2018.02.16.0001"
        }, 
        {
            "EventName" : "Date of Update",
            "EventValue" : "2018-12-31"
        }, 
        {
            "EventName" : "Link to Document",
            "EventValue" : "HTTP://WWW.PRORATA-NOW.COM"
        }
    ]
}
,
{
    "_id" : ObjectId("5d108816b6bc8d3280d082b2"),
    "asset_id" : "1000015",
    "Source" : "sapwarrantyrecall",
    "Ts" : "2019-06-24T08:21:41.400035+00:00",
    "Seq" : 277,
    "source" : "sapwarrantyrecall",
    "offset" : 277,
    "_clmno" : "000440000120",
    "AssetType" : "AGG",
    "Type" : "K I F",
    "Details" : [ 
        {
            "EventName" : "Name of Modification",
            "EventValue" : "2018.02.16.0001"
        }, 
        {
            "EventName" : "Date of Update",
            "EventValue" : "2018-12-31"
        }, 
        {
            "EventName" : "Link to Document",
            "EventValue" : "HTTP://WWW.PRORATA-NOW.COM"
        }
    ]
},
{
    "_id" : ObjectId("5d10881fb6bc8d3280d082b3"),
    "asset_id" : "1000020",
    "Source" : "sapwarrantyrecall",
    "Ts" : "2019-06-24T08:21:50.214035+00:00",
    "Seq" : 375,
    "source" : "sapwarrantyrecall",
    "offset" : 375,
    "_clmno" : "000440000120",
    "AssetType" : "AGG",
    "Type" : "K I F",
    "Details" : [ 
        {
            "EventName" : "Name of Modification",
            "EventValue" : "2018.02.16.0001"
        }, 
        {
            "EventName" : "Date of Update",
            "EventValue" : "2018-12-31"
        }, 
        {
            "EventName" : "Link to Document",
            "EventValue" : "HTTP://WWW.PRORATA-NOW.COM"
        }
    ]
}}])"""

import zlib, json, base64

ZIPJSON_KEY = 'base64(zip(o))'

def json_zip(j):

    j = {
        ZIPJSON_KEY: base64.b64encode(
            zlib.compress(
                json.dumps(j).encode('utf-8')
            )
        ).decode('ascii')
    }

    return j


# import zlib, json, base64

# ZIPJSON_KEY = 'base64(zip(o))'

def json_unzip(j, insist=True):
    try:
        assert (j[ZIPJSON_KEY])
        assert (set(j.keys()) == {ZIPJSON_KEY})
    except:
        if insist:
            raise RuntimeError("JSON not in the expected format {" + str(ZIPJSON_KEY) + ": zipstring}")
        else:
            return j

    try:
        j = zlib.decompress(base64.b64decode(j[ZIPJSON_KEY]))
    except:
        raise RuntimeError("Could not decode/unzip the contents")

    try:
        j = json.loads(j)
    except:
        raise RuntimeError("Could interpret the unzipped contents")

    return j


print(inputString)
# print(len(inputString))
print(sys.getsizeof(inputString))
print(json_zip(inputString))
print(type(json_zip(inputString)))
# print(len(json_zip(inputString)))
print(sys.getsizeof(json_zip(inputString)))
print(json_unzip(json_zip(inputString)))
# print(len(json_unzip(json_zip(inputString))))
print(sys.getsizeof(json_unzip(json_zip(inputString))))
print(type(json_unzip(json_zip(inputString))))
