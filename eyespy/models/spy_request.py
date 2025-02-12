from pydantic import BaseModel


class SpyRequest(BaseModel):
    spy_id: int
    spy_user_id: int
    spy_target_id: int
