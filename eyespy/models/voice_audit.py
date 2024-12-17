from datetime import datetime
from typing_extensions import TypedDict


class VoiceAudit(TypedDict, total=False):
    _id: str
    channel: str
    channel_id: int
    user: str
    user_id: int
    join_time: datetime
    leave_time: datetime
