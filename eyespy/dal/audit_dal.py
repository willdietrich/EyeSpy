import logging
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
        self.logger = logging.getLogger(__name__)

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

    def backfill_dwell_time(self):
        updated_count = 0
        audits_to_update = self.collection.find({})
        for audit in audits_to_update:
            join_time = audit.get("join_time")
            leave_time = audit.get("leave_time")

            if join_time is not None and leave_time is not None:
                dwell_time = int((leave_time - join_time).total_seconds())
                try:
                    self.collection.update_one(
                        {"_id": audit["_id"]},
                        {"$set": {"dwell_time": dwell_time}}
                    )
                    self.logger.info(f"Updated audit record with _id: {audit['_id']}, dwell_time: {dwell_time}")
                    updated_count += 1
                except Exception as e:
                    self.logger.error(f"Error updating audit record with _id: {audit['_id']}: {e}")

        return updated_count
