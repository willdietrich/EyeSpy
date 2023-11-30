import hikari
from hikari.presences import Status

from dal import AuditDal
import models as models


class EyeSpyAuditManager:
    def __init__(self, dal: AuditDal):
        self.dal = dal

    def add_spy(self, request: models.SpyRequest) -> bool:
        return True

    def shutdown(self):
        self.dal.client.close()
