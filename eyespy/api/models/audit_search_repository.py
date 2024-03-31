from typing import List

from pydantic import BaseModel

from eyespy.models.voice_audit import VoiceAudit


class AuditSearchResponse(BaseModel):
    results: List[VoiceAudit]
