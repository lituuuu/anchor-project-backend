from pymongo import MongoClient
from api import config

cluster = MongoClient(config.mongodb_url)
db = cluster["AnchorChallenger"]
collection = db["user"]

def insert(user, email, password):
    # unique index in mongodb collection
    collection.insert_one({"username": user, "email": email, "password": password})
    return True


def get(user, password):
    # unique index in mongodb collection
    valor = collection.find_one({"username": user, "password": password})
    return valor




