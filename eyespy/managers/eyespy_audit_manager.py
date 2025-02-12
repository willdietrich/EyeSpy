from datetime import datetime

import hikari
from hikari.api import RESTClient

from eyespy.dal.audit_dal import AuditDal
from eyespy.models.voice_audit import VoiceAudit


class EyeSpyAuditManager:
    def __init__(self, dal: AuditDal):
        self.dal = dal

    def _assign_dwell_time(self, voice_audit: VoiceAudit, old_voice_audit: VoiceAudit) -> int:
        if voice_audit is not None and old_voice_audit is not None and hasattr(voice_audit, 'join_time') and hasattr(old_voice_audit, 'leave_time'):
            diff = voice_audit.join_time - old_voice_audit.leave_time
            old_voice_audit.dwell_time = int(abs(diff.total_seconds()))

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

        self._assign_dwell_time(voice_audit, old_voice_audit)

        if old_voice_audit is not None and voice_audit is not None:
            matching_audit_cursor = self.dal.find_matching_audit(old_voice_audit)
            matching_audit = matching_audit_cursor.next()
            if matching_audit is not None:
                self.dal.upsert_audit_record(matching_audit, old_voice_audit)

            self.dal.insert_audit_record(voice_audit)
        elif old_voice_audit is not None and voice_audit is None:
            matching_audit_cursor = self.dal.find_matching_audit(old_voice_audit)
            matching_audit_dict = matching_audit_cursor.next()
            matching_audit = VoiceAudit.model_validate(matching_audit_dict)
            self._assign_dwell_time(matching_audit, old_voice_audit)
            if matching_audit is not None:
                self.dal.upsert_audit_record(matching_audit, old_voice_audit)
        elif old_voice_audit is None and voice_audit is not None:
            self.dal.insert_audit_record(voice_audit)
        else:
            return False

        return True

    def shutdown(self):
        self.dal.client.close()
