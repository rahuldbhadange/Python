import pymongo
import pprint


client = pymongo.MongoClient("mongodb://localhost:27017/")

blogDatabase = client.blog
usersCollection = blogDatabase.users
articlesCollection = blogDatabase.articles

randomUser = usersCollection.find_one()

print(randomUser)

karmaCount = usersCollection.find({"karma": 450}).count()  # {"$gte": 450, "$lte": 475}
print(karmaCount)
# karmaCount = usersCollection.find({"karma": 450})  # {"$gte": 450, "$lte": 475}
karmaCount1 = usersCollection.count_documents({"karma": 450})
print(karmaCount1)

# for y in karmaCount:
#     print(karmaCount)

# Add Comments to an article

# articlesCollection.update({"_id": 19}, {"$set": {"comments": []}})

# Update Comments

# articlesCollection.update({"_id": 19},
#                           {"$push": {"comments":
#                                          {"username": "mary",
#                                           "comment": "Great first post."}}})

# Delete Article

# articlesCollection.remove({"_id": 25})


