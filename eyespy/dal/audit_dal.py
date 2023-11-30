from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection


class AuditDal:
    def __init__(self, client: MongoClient, db: Database, collection: Collection, *args, **kwargs):
        self.client = client
        self.db = db
        self.collection = collection
