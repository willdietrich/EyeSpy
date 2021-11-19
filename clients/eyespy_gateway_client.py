import logging

import hikari
import lightbulb
from lightbulb import commands

import managers
from models import SpyRequest
from models import NotifySpyRequest


class EyeSpyClient(lightbulb.BotApp):
    def __init__(self, manager: managers.EyeSpyManager, token: str, *args, **kwargs):
        self.manager = manager
        super().__init__(intents=hikari.Intents.ALL, token=token, default_enabled_guilds=195357021300719616)

        # Initialize events
        self.event_manager.subscribe(hikari.StartingEvent, self.on_starting)
        self.event_manager.subscribe(hikari.StartedEvent, self.on_started)
        self.event_manager.subscribe(hikari.StoppingEvent, self.on_stopping)
        self.event_manager.subscribe(hikari.DMMessageCreateEvent, self.on_message)
        self.event_manager.subscribe(hikari.PresenceUpdateEvent, self.presence_update)

        # Initialize commands
        self.command(self.follow)

        self.logger = logging.getLogger('hikari.bot')
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(filename='./discord.log', encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.logger.addHandler(handler)

    # Gateway listeners
    async def on_starting(self, event: hikari.StartingEvent):
        self.logger.info('Starting up')

    async def on_started(self, event: hikari.StartedEvent):
        self.logger.info('Started')

    async def on_stopping(self, event: hikari.StoppingEvent):
        self.logger.info('Stopping')

    async def on_message(self, event: hikari.DMMessageCreateEvent):
        self.logger.info('Message received: {0}'.format(event.message))

    async def presence_update(self, event: hikari.PresenceUpdateEvent):
        req = NotifySpyRequest(status_change_user_id=event.user_id, status=event.presence.visible_status)
        await self.manager.notify_spies(self.rest, req)


    # Commands
    @lightbulb.option("discordid", "Who to follow")
    @lightbulb.command("follow", "Follow someones status online")
    @lightbulb.implements(commands.SlashCommand)
    async def follow(ctx: lightbulb.context.Context):
        req = SpyRequest(spy=int(ctx.member.id), spy_id=None, spy_target=int(ctx.options.discordid))
        if ctx.app.manager.add_spy(req):
            requester = await ctx.app.rest.fetch_user(req.spy)
            target = await ctx.app.rest.fetch_user(req.spy_target)
            await ctx.respond(f"{requester.username}#{requester.discriminator} is now following {target.username}#{target.discriminator}")
        else:
            await ctx.respond("Unable to follow user, or you are already following them")
