from pymongo import MongoClient
from api import config

cluster = MongoClient(config.mongodb_url)
db = cluster["AnchorChallenger"]
collection = db["user"]

def insert(user, email, password):
    try :
        # unique index in mongodb collection
        collection.insert_one({"username": user, "email": email, "password": password})
        return True
    except Exception as e:
        print (e)
        return False

def get(user, password):
    try:
        # unique index in mongodb collection
        valor = collection.find_one({"username": user, "password": password})
        return valor
    except Exception as e:
        print ("huasdhu")
        return None




