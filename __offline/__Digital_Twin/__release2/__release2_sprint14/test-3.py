

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





















import sys
import msgpack

print(msgpack.packb(inputString))
print(type(msgpack.packb(inputString)))
print(sys.getsizeof(msgpack.packb(inputString)))


print(msgpack.unpackb(msgpack.packb(inputString)))
print(type(msgpack.unpackb(msgpack.packb(inputString))))
print(sys.getsizeof(msgpack.unpackb(msgpack.packb(inputString))))













# import sys
#
# import msgpack
# print(msgpack.unpackb(msgpack.packb([b'spam', u'eggs'])))
# print(type(msgpack.unpackb(msgpack.packb([b'spam', u'eggs']))))
# print(sys.getsizeof(msgpack.unpackb(msgpack.packb([b'spam', u'eggs']))))
# # [b'spam', b'eggs']
# print(msgpack.unpackb(msgpack.packb([b'spam', u'eggs'], use_bin_type=True), raw=False))
# print(type(msgpack.unpackb(msgpack.packb([b'spam', u'eggs'], use_bin_type=True), raw=False)))
# print(sys.getsizeof(msgpack.unpackb(msgpack.packb([b'spam', u'eggs'], use_bin_type=True), raw=False)))
# # [b'spam', 'eggs']





# import sys
#
# import msgpack
# print(msgpack.packb([b'spam', u'eggs']))
# print(type(msgpack.packb([b'spam', u'eggs'])))
# print(sys.getsizeof(msgpack.packb([b'spam', u'eggs'])))
#
#
# print(msgpack.unpackb(msgpack.packb([b'spam', u'eggs'])))
# print(type(msgpack.unpackb(msgpack.packb([b'spam', u'eggs']))))
# print(sys.getsizeof(msgpack.unpackb(msgpack.packb([b'spam', u'eggs']))))




# [b'spam', b'eggs']
# print(msgpack.unpackb(msgpack.packb([b'spam', u'eggs'], use_bin_type=True), raw=False))
# print(type(msgpack.unpackb(msgpack.packb([b'spam', u'eggs'], use_bin_type=True), raw=False)))
# print(sys.getsizeof(msgpack.unpackb(msgpack.packb([b'spam', u'eggs'], use_bin_type=True), raw=False)))
# # [b'spam', 'eggs']





