from dataclasses import dataclass


@dataclass
class SpyRequest:
    spy_id: int
    spy_user_id: int
    spy_target_id: int
