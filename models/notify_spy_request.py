from dataclasses import dataclass


@dataclass
class NotifySpyRequest:
    status_change_user_id: int
    status: str