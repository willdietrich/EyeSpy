import hikari

from dal import Dal
import models


class EyeSpyManager:
    def __init__(self, dal: Dal):
        self.dal = dal

    def add_spy(self, request: models.SpyRequest) -> bool:
        matches = self.dal.check_target_exists(request)
        if len(matches) > 0:
            return False

        spy_id = self.dal.get_spy_id(request)
        if len(spy_id) > 0:
            request.spy_id = spy_id[0]
        else:
            request.spy_id = self.dal.insert_spy(request)
        self.dal.insert_target(request)

        return True

    async def notify_spies(self, restApi: hikari.api.RESTClient, request: models.NotifySpyRequest):
        user = await restApi.fetch_user(request.status_change_user_id)
        notifications = self.dal.get_spies(request)
        for notification in notifications:
            notification_id = notification[0]
            channel = await restApi.create_dm_channel(notification_id)
            await restApi.create_message(channel, f'{user.username} is now {request.status}')
