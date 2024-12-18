from datetime import datetime

import hikari
from hikari.api import RESTClient

from eyespy.dal.audit_dal import AuditDal
from eyespy.models.voice_audit import VoiceAudit


class EyeSpyAuditManager:
    def __init__(self, dal: AuditDal):
        self.dal = dal

    async def persist_voice_audit(self, rest: RESTClient, event: hikari.VoiceStateUpdateEvent) -> bool:
        voice_audit = None
        old_voice_audit = None

        if event.state.channel_id is None and event.old_state.channel_id is None:
            return False

        user = await rest.fetch_user(event.state.user_id)

        if event.state is not None and event.state.channel_id is not None:
            channel = await rest.fetch_channel(event.state.channel_id)
            voice_audit = VoiceAudit(channel=channel.name,
                                     channel_id=event.state.channel_id,
                                     user=user.username,
                                     user_id=event.state.user_id,
                                     join_time=datetime.utcnow())

        if event.old_state is not None:
            old_channel = await rest.fetch_channel(event.old_state.channel_id)
            old_voice_audit = VoiceAudit(channel=old_channel.name,
                                         channel_id=event.old_state.channel_id,
                                         user=user.username,
                                         user_id=event.state.user_id,
                                         leave_time=datetime.utcnow())

        if old_voice_audit is not None and voice_audit is not None:
            matching_audit_cursor = self.dal.find_matching_audit(old_voice_audit)
            matching_audit = matching_audit_cursor.next()
            if matching_audit is not None:
                self.dal.upsert_audit_record(matching_audit, old_voice_audit)

            self.dal.insert_audit_record(voice_audit)
            #TODO left a channel and went to a new one
        elif old_voice_audit is not None and voice_audit is None:
            matching_audit_cursor = self.dal.find_matching_audit(old_voice_audit)
            matching_audit = matching_audit_cursor.next()
            if matching_audit is not None:
                self.dal.upsert_audit_record(matching_audit, old_voice_audit)
            #TODO left all voice channels
        elif old_voice_audit is None and voice_audit is not None:
            self.dal.insert_audit_record(voice_audit)
            #TODO joined voice channel for the first time
        else:
            return False

        return True

    def shutdown(self):
        self.dal.client.close()
