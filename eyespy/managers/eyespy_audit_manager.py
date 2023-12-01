import json
from datetime import datetime

import hikari
from hikari.api import RESTClient
from hikari.presences import Status

import dal
from dal import AuditDal
from models import VoiceAudit


class EyeSpyAuditManager:
    def __init__(self, dal: AuditDal):
        self.dal = dal

    async def persist_voice_audit(self, rest: RESTClient, event: hikari.VoiceStateUpdateEvent) -> bool:
        if event.state.channel_id is None:
            return False

        channel = await rest.fetch_channel(event.state.channel_id)
        user = await rest.fetch_user(event.state.user_id)
        voice_audit = VoiceAudit(channel=channel.name,
                                 channel_id=event.state.channel_id,
                                 user=user.username,
                                 user_id=event.state.user_id,
                                 join_time=datetime.utcnow())
        self.dal.insert_audit_record(voice_audit)
        return True

    def shutdown(self):
        self.dal.client.close()
