import pymongo
from pprint import pprint

Client = pymongo.MongoClient("mongodb://localhost:27017/")


# creating database
DB = Client.database2019
CO = DB.collection2019
DB_list = Client.list_database_names()
print("Name of the databases exist before:", DB_list)
if "database2019" in DB_list:
    print("The Database is already exists")
print("Name of the databases exist after:", DB_list)


# creating collection i.e. table
collection10 = DB["collection10"]
COL_list = DB.list_collection_names()
print("Name of the collections exist before:", COL_list)
if "collection2019" in COL_list:
    print("The Collection is already exists")
print("Name of the collections exist after:", COL_list)

# P = {"Day": "Monday", "Date": 2, "Month": "December", "Year": 1991}
#
# try:
#     P = DB.collection2019.insert_one(P)
# except Exception as EX:
#     print("Error is: ", EX)

# pprint(DB.collection2019.find_one({"Date": 2}))
pprint(DB.collection2019.find())
