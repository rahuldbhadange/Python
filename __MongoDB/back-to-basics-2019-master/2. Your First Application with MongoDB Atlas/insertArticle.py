import datetime
import pymongo
import pprint

# client = pymongo.MongoClient("mongodb+srv://kenalger:SuperPassword@blog-i6lut.mongodb.net/test?retryWrites=true")
client = pymongo.MongoClient("mongodb://localhost:27017/")


blogDatabase = client.blog
usersCollection = blogDatabase.users
articlesCollection = blogDatabase.articles

author = 'kalger'

article = {
    "title": "My first post",
    "body": "The body of the amazing post would go here.",
    "author": author,
    "tags": ["ken", "general", "admin", "Oregon"],
    "posted": datetime.datetime.now()
}

# Let's check to make sure the author exists before inserting

usersCollection.username(author)
# usersCollection.insert_one(article)
# if usersCollection.find_one({"username": author}):
if usersCollection.find_one({"author": author}):
    document = articlesCollection.insert_one(article)
    pprint.pprint(article)
else:
    raise ValueError("Author {} is not a current user".format(author))

