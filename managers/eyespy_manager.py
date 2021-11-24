import hikari
from hikari.presences import Status

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

    def remove_spy(self, request: models.SpyRequest) -> bool:
        matches = self.dal.check_target_exists(request)
        if len(matches) < 1:
            return False

        request.spy_id = matches[0][0]
        self.dal.delete_target(request)

        return True

    def list_spy(self, discord_id: int) -> [(str,)]:
        results = self.dal.get_spies_for_user(discord_id)

        if len(results) < 0:
            return []

        matches = []
        for follow in results:
            matches.append(follow[0])

        return matches

    async def notify_spies(self, restApi: hikari.api.RESTClient, request: models.NotifySpyRequest) -> bool:
        if not self.should_notify_status_change(request.status):
            return False
        user = await restApi.fetch_user(request.status_change_user_id)
        notifications = self.dal.get_spies(request)
        for notification in notifications:
            notification_id = notification[0]
            channel = await restApi.create_dm_channel(notification_id)
            await restApi.create_message(channel, f'{user.username} is now {request.status}')

        return True

    def should_notify_status_change(self, status: Status) -> bool:
        # Only print
        if status == Status.ONLINE:
            return True

        # TODO More complex logic here

        return False
