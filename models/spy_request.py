from dataclasses import dataclass


@dataclass
class SpyRequest:
    spy: int
    spy_id: int
    spy_target: int
