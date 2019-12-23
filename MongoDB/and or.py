from pprint import pprint
import pymongo

Client = pymongo.MongoClient("mongodb://localhost:27017/")

db = Client.database2019

Result = db.collection2019.find({
    "$and": [
        {"$or":
            [{"name": "Ram"}, {"last_name": "john"}]}
        ,
        {"status": "A"}
    ]
}
)

for result in Result:
    pprint(result)


# database2019.collection10({
#     $ and:[
#         {
#     $ or: [
#         {"first_name": "john"},
#         {"last_name": "john"}
#     ]
#     },
#     {
#         "Phone": "12345678"
#     }
#     ]
#     } )
