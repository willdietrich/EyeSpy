import logging

import hikari
import lightbulb
from lightbulb import commands
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.trace import StatusCode

from eyespy.managers.eyespy_audit_manager import EyeSpyAuditManager
from eyespy.managers.eyespy_manager import EyeSpyManager
from eyespy.models.notify_spy_request import NotifySpyRequest
from eyespy.models.spy_request import SpyRequest


class EyeSpyClient(lightbulb.BotApp):
    manager: EyeSpyManager
    audit_manager: EyeSpyAuditManager
    token: str

    def __init__(self, manager: EyeSpyManager, audit_manager: EyeSpyAuditManager, token: str, *args, **kwargs):
        self.manager = manager
        self.audit_manager = audit_manager
        self.token = token
        super().__init__(intents=hikari.Intents.ALL, token=token, default_enabled_guilds=195357021300719616)

        # Initialize events
        # region Events
        self.event_manager.subscribe(hikari.StartingEvent, self.on_starting)
        self.event_manager.subscribe(hikari.StartedEvent, self.on_started)
        self.event_manager.subscribe(hikari.StoppingEvent, self.on_stopping)
        self.event_manager.subscribe(hikari.DMMessageCreateEvent, self.on_message)
        self.event_manager.subscribe(hikari.PresenceUpdateEvent, self.presence_update)
        self.event_manager.subscribe(hikari.VoiceStateUpdateEvent, self.audit_channel_event)
        # endregion

        # Initialize commands
        # region Commands
        self.command(self.follow)
        self.command(self.unfollow)
        self.command(self.list)

        # endregion

        # region Logging setup
        self.logger = logging.getLogger('hikari.bot')
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(filename='../discord.log', encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.logger.addHandler(handler)
        # endregion

        # Initialize the span manager
        provider = TracerProvider()
        processor = BatchSpanProcessor(ConsoleSpanExporter())
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)
        tracer = trace.get_tracer("eyespy.bot.tracer")
        self.tracer = tracer

    # Gateway listeners
    # region Listeners
    async def on_starting(self, event: hikari.StartingEvent):
        self.logger.info('Starting up')

    async def on_started(self, event: hikari.StartedEvent):
        self.logger.info('Started')

    async def on_stopping(self, event: hikari.StoppingEvent):
        self.logger.info('Stopping')
        self.audit_manager.shutdown()

    async def on_message(self, event: hikari.DMMessageCreateEvent):
        self.logger.info('Message received: {0}'.format(event.message))

    async def presence_update(self, event: hikari.PresenceUpdateEvent):
        with self.tracer.start_as_current_span("presence_update") as span:
            span.set_attribute("user_id", str(event.user_id))

            req = NotifySpyRequest(status_change_user_id=event.user_id, status=event.presence.visible_status)
            await self.manager.notify_spies(self.rest, req)

            span.set_status(StatusCode.OK)

    async def audit_channel_event(self, event: hikari.VoiceStateUpdateEvent):
        await self.audit_manager.persist_voice_audit(self.rest, event)
    # endregion

    # Commands
    # region EyeSpy commands
    @lightbulb.option("discordid", "Who to follow")
    @lightbulb.command("follow", "Follow a users online status")
    @lightbulb.implements(commands.SlashCommand)
    async def follow(ctx: lightbulb.Context) -> None:
        with ctx.app.tracer.start_as_current_span("command_follow") as span:
            try:
                req = SpyRequest(spy_user_id=int(ctx.member.id), spy_id=None, spy_target_id=int(ctx.options.discordid))
                target = await ctx.app.rest.fetch_user(req.spy_target_id)
                span.set_attribute("requester", str(ctx.member.id))
                span.set_attribute("target", str(ctx.options.discordid))
                if ctx.app.manager.add_spy(req):
                    requester = await ctx.app.rest.fetch_user(req.spy_user_id)
                    await ctx.respond(f"{str(requester)} is now following {str(target)}")
                    span.set_status(StatusCode.OK)
                else:
                    await ctx.respond("Unable to follow user, or you are already following them")
                    span.set_status(StatusCode.ERROR)
            except:
                await ctx.respond("An error occurred while attempting to follow the specified user, make sure the specified ID is correct.")
                span.set_status(StatusCode.ERROR)

    @lightbulb.option("discordid", "Who to unfollow")
    @lightbulb.command("unfollow", "Stop following a user")
    @lightbulb.implements(commands.SlashCommand)
    async def unfollow(ctx: lightbulb.Context) -> None:
        with ctx.app.tracer.start_as_current_span("command_unfollow") as span:
            try:
                req = SpyRequest(spy_user_id=int(ctx.member.id), spy_id=None, spy_target_id=int(ctx.options.discordid))
                span.set_attribute("requester", str(ctx.member.id))
                span.set_attribute("target", str(ctx.options.discordid))
                if ctx.app.manager.remove_spy(req):
                    requester = await ctx.app.rest.fetch_user(req.spy_user_id)
                    target = await ctx.app.rest.fetch_user(req.spy_target_id)
                    await ctx.respond(f"{str(requester)} is no longer following {str(target)}")
                    span.set_status(StatusCode.OK)
                else:
                    await ctx.respond("Unable to un-follow, or you never previously followed that user")

            except:
                await ctx.respond("An error occurred while attempting to unfollow the specified user, make sure the specified ID is correct.")
                span.set_status(StatusCode.ERROR)

    @lightbulb.command("list", "List what users you are following")
    @lightbulb.implements(commands.SlashCommand)
    async def list(ctx: lightbulb.Context) -> None:
        with ctx.app.tracer.start_as_current_span("command_list") as span:
            span.set_attribute("requester", str(ctx.member.id))
            spies = ctx.app.manager.list_spy(int(ctx.member.id))
            if spies == None or len(spies) < 1:
                await ctx.respond(f"It doesn't appear that you are currently following anyone, try `/follow`")
                span.set_status(StatusCode.OK)
                return

            result = []
            for spy in spies:
                target = await ctx.app.rest.fetch_user(spy)
                result.append((f"{target.username}#{target.discriminator}", spy))

            await ctx.respond(f"You are following: {result}")
            span.set_status(StatusCode.OK)
    # endregion
