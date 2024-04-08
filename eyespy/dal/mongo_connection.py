import os

from pymongo import MongoClient


def get_mongo_connection():
    mongodb_client = MongoClient(os.getenv('MONGODB_URI'))
    mongodb_db = mongodb_client[os.getenv('MONGODB_DB')]
    mongodb_audit_collection = mongodb_db[os.getenv('MONGODB_AUDIT_COLLECTION')]

    return {
        "client": mongodb_client,
        "db": mongodb_db,
        "collection": mongodb_audit_collection,
    }
