from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
import json

from models import VoiceAudit


class AuditDal:
    def __init__(self, client: MongoClient, db: Database, collection: Collection, *args, **kwargs):
        self.client = client
        self.db = db
        self.collection = collection

    def insert_audit_record(self, audit_json: VoiceAudit):
        self.collection.insert_one(audit_json)