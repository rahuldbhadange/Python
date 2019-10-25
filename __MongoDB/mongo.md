    import pymongo
    
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb["customers"]


**Create:**
    
    1. insert_one()
    2. insert_many()

**Read:**

    1. find_one()
    2. find()

**Update:**

    1. update_one()
    2. update_many()

**Delete:**
    
    1. delete_one()
    2. delete_many()



