import pymongo
# pprint library is used to make the output look more pretty
from pprint import pprint

# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string

Client = pymongo.MongoClient("mongodb://localhost:27017/")


# creating database
DB = Client["database2019"]
DB = Client.database2019
# COL = database2019.collection2019
DB_list = Client.list_database_names()
print("Name of the databases exist before:", DB_list)
if "database10" in DB_list:
    print("The Database is already exists")
print("Name of the databases exist after:", DB_list)


# creating collection i.e. table
collection10 = DB["collection10"]
COL_list = DB.list_collection_names()
print("Name of the collections exist before:", COL_list)
if "collection10" in COL_list:
    print("The Collection is already exists")
print("Name of the collections exist after:", COL_list)

# P = [
#           # {
#           #     "_id": 1,
#           #     "name": "Ram",
#           #     "age": 34,
#           #     "type": 1,
#           #     "status": "A",
#           #     "favorites": {"artist": "billy", "food": "pastry"},
#           #     "finished": [9, 1],
#           #     "badges": ["olive", "red"],
#           #     "points": [
#           #         {"points": 75, "bonus": 15},
#           #         {"points": 85, "bonus": 9}
#           #     ]
#           # },
#           # {
#           #     "_id": 2,
#           #     "name": "Mohan",
#           #     "age": 35,
#           #     "type": 2,
#           #     "status": "B",
#           #     "favorites": {"artist": "alia", "food": "pan cakes"},
#           #     "finished": [8, 9],
#           #     "badges": ["brown", "grey"],
#           #     "points": [
#           #         {"points": 95, "bonus": 5},
#           #         {"points": 91, "bonus": 3}
#           #     ]
#           # },
#             {
#                 "_id": 3,
#                 "name": "Rakesh",
#                 "age": 39,
#                 "type": 8,
#                 "status": "C",
#                 "favorites": {"artist": "Ranbir", "food": "Biryani"},
#                 "finished": [3, 7],
#                 "badges": ["white", "red"],
#                 "points": [
#                     {"points": 45, "bonus": 7},
#                     {"points": 84, "bonus": 3}
#                 ]
#             },
#             {
#                 "_id": 4,
#                 "name": "Ronny",
#                 "age": 39,
#                 "type": 8,
#                 "status": "C",
#                 "favorites": {"artist": "Salman", "food": "Rice"},
#                 "finished": [4, 8],
#                 "badges": ["Black", "red"],
#                 "points": [
#                     {"points": 67, "bonus": 8},
#                     {"points": 74, "bonus": 5}
#                 ]
#             }
# ]
# #
# try:
#     P = DB.collection2019.insert_many(P)
# except Exception as EX:
#     print("Error is: ", EX)


# Z = COL.find({"status": "A"})
# pprint(Z)
#
# X = COL.find({"age": 25})
# pprint(X)
#
# Z = DB.collection2019.find({"status": {$in:[ "P", "D" ]}})
# # pprint("status 'A' data: ", Z)

# for Y in DB.collection2019.find():
#     print(Y)
#     print(type(Y))

Z = DB.collection2019.find({"status": {"$in": [ "C", "A" ]}})

# import json
# print(json.loads(Z))
# print(type(Z))

for z in Z:
    pprint(z)
