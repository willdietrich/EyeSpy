from datetime import datetime

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from eyespy.models.voice_audit import VoiceAudit


class AuditDal:
    def __init__(self, client: MongoClient, db: Database, collection: Collection, *args, **kwargs):
        self.client = client
        self.db = db
        self.collection = collection

    def insert_audit_record(self, audit_json: VoiceAudit):
        self.collection.insert_one(audit_json.model_dump(exclude_none=True))

    def find_matching_audit(self, audit_json: VoiceAudit):
        return self.collection.find({
            "channel_id": audit_json.channel_id,
            "user_id": audit_json.user_id,
            "leave_time": {"$exists": False},
        }).sort("join_time", -1)

    def upsert_audit_record(self, matching_audit: VoiceAudit, audit_json: VoiceAudit):
        return self.collection.update_one({
            "_id": matching_audit.id
        }, {
            "$set": {
                "leave_time": audit_json.leave_time,
                "dwell_time": audit_json.dwell_time
            }
        })

    def search_audit_channels(self, target: str | None, timeframe_days: datetime | None):
        query = {}
        if target is not None:
            query['channel_id'] = float(target)

        if timeframe_days is not None:
            query['leave_time'] = {"$gte": timeframe_days}

        cursor = self.collection.find(query)
        return cursor
