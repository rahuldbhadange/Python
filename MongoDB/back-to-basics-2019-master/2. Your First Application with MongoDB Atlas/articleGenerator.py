import datetime
import pymongo
import random
import string
# import pprint


def randomString(size, letters=string.ascii_letters):
    return "".join([random.choice(letters) for _ in range(size)])


def makeArticle(count):
    return {
        "_id": count,
        "title": "Title " + str(count),
        "topic": randomString(10),
        "author": "USER_" + str(randomString(9)),
        "posted": datetime.datetime.now(),
        "page no": random.randint(1, 8)
    }

def makeUser(count):
    return {
        "_id": "USER_" + str(count),
        "password": randomString(3),
        "city": randomString(5),
        "registered": datetime.datetime.now(),
        "lang": "EN",
        "mobile no": random.randint(0, 1234567890)
    }


client = pymongo.MongoClient("mongodb://localhost:27017/")

newsDatabase = client.news
usersCollection = newsDatabase.users
articlesCollection = newsDatabase.articles

usersCollection.drop()
articlesCollection.drop()

users = []
count = 0
for i in range(10):
    users.append(makeUser(i))
    if (len(users) % 10) == 0:
        usersCollection.insert_many(users)
        count = count + 10
        print("Inserted {} users".format(count))
        users = []

articles = []
count = 0

for i in range(10):
    articles.append(makeArticle(i))
    if (len(articles) % 10) == 0:
        articlesCollection.insert_many(articles)
        count = count + 10
        print("Inserted {} articles".format(articles))
        articles = []
