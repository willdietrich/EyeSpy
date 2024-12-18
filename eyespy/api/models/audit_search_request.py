from pydantic import BaseModel

from eyespy.enumerations.audit_type import AuditType


class AuditSearchRequest(BaseModel):
    target: str | None
    type: AuditType
    timeframe_days: int | None
