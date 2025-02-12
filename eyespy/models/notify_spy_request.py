from pydantic import BaseModel


class NotifySpyRequest(BaseModel):
    status_change_user_id: int
    status: str