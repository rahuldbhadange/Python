import pymongo
# pprint library is used to make the output look more pretty
from pprint import pprint

# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
# mongodb://mongodb0.example.com:27017/admin
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# Issue the serverStatus command and print the results
# serverStatusResult = myDB.command("serverStatus")
# pprint(serverStatusResult)


# creating database
DB = myclient["new_database"]
DBlist = myclient.list_database_names()
print("Name of the databases exist before:", DBlist)
if "new_database" in DBlist:
    print("The Database is already exists")
print("Name of the databases exist after:", DBlist)


# creating collection i.e. table
COL = DB["new_collection"]
COLlist = DB.list_collection_names()
print("Name of the collections exist before:", COLlist)
if "new_collection" in COLlist:
    print("The Collection is already exists")
print("Name of the collections exist after:", COLlist)


P = DB.COL.insertMany(
  [
     {
       "_id": 1,
       "name": "sue",
       "age": 19,
       type: 1,
       "status": "P",
       "favorites": {"artist": "Picasso", "food": "pizza"},
       "finished": [7, 3],
       "badges": ["blue", "black"],
       "points": [
          {"points": 85, "bonus": 20},
          {"points": 85, "bonus": 10}
       ]
     },
     {
       "_id": 2,
       "name": "rooney",
       "age": 20,
       type: 2,
       "status": "C",
       "favorites": {"artist": "Cassatt", "food": "cake"},
       "finished": [8, 4],
       "badges": ["pink", "green"],
       "points": [
          {"points": 95, "bonus": 8},
          {"points": 95, "bonus": 5}
       ]
     },
      {
          "_id": 3,
          "name": "sean",
          "age": 25,
          type: 1,
          "status": "A",
          "favorites": {"artist": "billy", "food": "pastry"},
          "finished": [9, 1],
          "badges": ["olive", "red"],
          "points": [
              {"points": 75, "bonus": 15},
              {"points": 85, "bonus": 9}
          ]
      },
  ]
)

# # insert single document
# mydict = {"Name": "Rahul", "Age": 27, "Degree": "BE", "Place": "Nashik", "Language": "Marathi", "Height": 168.5, "Color" : "Wheatish"}
# x = mycol.insert_one(mydict)
# print(x.inserted_id)
#
# # insert multiple documents
# mylist = [
#     {"Name": "Rahul", "Age": 27},
#     {"Degree": "BE", "Place": "Nashik"},
#     {"Language": "Marathi", "Height": 168.5}
#     ]
#
# x = mycol.insert_many(mylist)
# # print list of the _id values of the inserted documents:
# print(x.inserted_ids)

# y = myDB1.mycol1.insert(
#     {
#         "name": "rashi",
#         "age": 22,
#         "status": "O",
#         "_id": 123456780
#         }
# )
# y = myDB1.mycol1.find_one()
# pprint(y)

Z = DB.COL.find({"status": "A"})
pprint("status:A ::", Z)

Z = DB.COL.find({"age": 25})
pprint("age:25 ::", Z)

for y in DB.COL.find():
    pprint(y)

# x = mycol.find_one()
# pprint(x)
# print(mycol.inserted_ids)

# for x in mycol.find():
#     pprint(x)

