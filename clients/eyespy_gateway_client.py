import logging

import hikari

from dal.dal import Dal


class EyeSpyClient(hikari.GatewayBot):
    def __init__(self, dal: Dal, token: str, *args, **kwargs):
        self.dal = dal
        super().__init__(intents=hikari.Intents.ALL, token=token)

        # Initialize events
        self.event_manager.subscribe(hikari.StartingEvent, self.on_starting)
        self.event_manager.subscribe(hikari.StartedEvent, self.on_started)
        self.event_manager.subscribe(hikari.StoppingEvent, self.on_stopping)
        self.event_manager.subscribe(hikari.DMMessageCreateEvent, self.on_message)
        self.event_manager.subscribe(hikari.PresenceUpdateEvent, self.presence_update)

        self.logger = logging.getLogger('hikari.bot')
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(filename='./discord.log', encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.logger.addHandler(handler)

    async def on_starting(self, event: hikari.StartingEvent):
        self.logger.info('Starting up', stack_info=True)

    async def on_started(self, event: hikari.StartedEvent):
        self.logger.info('Started', stack_info=True)

    async def on_stopping(self, event: hikari.StoppingEvent):
        self.logger.info('Stopping', stack_info=True)

    async def on_message(self, event: hikari.DMMessageCreateEvent):
        self.logger.info('Message received: {0}'.format(event.message), stack_info=True)
        if event.content.lower().startswith("ping"):
            await event.message.respond("Pong!")
        if event.content.lower() == "chungus":
            await event.message.respond("He's a great big boi.")

    async def presence_update(self, event: hikari.PresenceUpdateEvent):
        self.logger.info('Update received. old presence: {0}, new presence: {1}'.format(event.old_presence, event.presence))
        user = await self.rest.fetch_user(event.user_id)
        self.logger.info('User Info: {0}'.format(user))
        # self.dal.insert_status(before, after)
