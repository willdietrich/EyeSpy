from dal import Dal
from models import SpyRequest


class EyeSpyManager:
    def __init__(self, dal: Dal):
        self.dal = dal

    def add_spy(self, request: SpyRequest) -> bool:
        spyid = self.dal.insert_spy(request)
        request.spyId = spyid
        self.dal.insert_target(request)

        return True