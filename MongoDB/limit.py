from pprint import pprint

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["news"]
mycol = mydb["users"]

myresult = mycol.find().limit(3)

# print the result:
for x in myresult:
    print()
    pprint(x)
