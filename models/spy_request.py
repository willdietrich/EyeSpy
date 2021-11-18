from dataclasses import dataclass


@dataclass
class SpyRequest:
    spy: int
    spyId: int
    spyTarget: int
