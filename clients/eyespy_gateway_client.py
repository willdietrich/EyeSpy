import logging

import hikari
import lightbulb
from lightbulb import commands

import managers
from models import SpyRequest
from models import NotifySpyRequest


class EyeSpyClient(lightbulb.BotApp):
    manager: managers.EyeSpyManager
    music_manager: managers.MusicManager
    token: str

    def __init__(self, manager: managers.EyeSpyManager, music_manager: managers.MusicManager, token: str, *args, **kwargs):
        self.manager = manager
        self.music_manager = music_manager
        self.token = token
        super().__init__(intents=hikari.Intents.ALL, token=token, default_enabled_guilds=195357021300719616)

        # Initialize events
        # region Events
        self.event_manager.subscribe(hikari.StartingEvent, self.on_starting)
        self.event_manager.subscribe(hikari.StartedEvent, self.on_started)
        self.event_manager.subscribe(hikari.StoppingEvent, self.on_stopping)
        self.event_manager.subscribe(hikari.DMMessageCreateEvent, self.on_message)
        self.event_manager.subscribe(hikari.PresenceUpdateEvent, self.presence_update)
        self.event_manager.subscribe(hikari.ShardReadyEvent, self.shard_ready)
        self.event_manager.subscribe(hikari.VoiceStateUpdateEvent, self.voice_state_update)
        self.event_manager.subscribe(hikari.VoiceServerUpdateEvent, self.voice_server_update)
        # endregion

        # Initialize commands
        # region Commands
        self.command(self.follow)
        self.command(self.unfollow)
        self.command(self.list)
        self.command(self.join_voice)
        self.command(self.leave_voice)
        self.command(self.play_song)
        self.command(self.stop_song)
        # endregion

        # region Logging setup
        self.logger = logging.getLogger('hikari.bot')
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(filename='./discord.log', encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.logger.addHandler(handler)
        # endregion

    # Gateway listeners
    # region Listeners
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

    async def shard_ready(self, event: hikari.ShardReadyEvent):
        await self.music_manager.start_lavalink(event, self.token)

    async def voice_state_update(self, event: hikari.VoiceStateUpdateEvent) -> None:
        self.music_manager.lavalink.raw_handle_event_voice_state_update(
            event.state.guild_id,
            event.state.user_id,
            event.state.session_id,
            event.state.channel_id,
        )

    async def voice_server_update(self, event: hikari.VoiceServerUpdateEvent) -> None:
        await self.music_manager.lavalink.raw_handle_event_voice_server_update(event.guild_id, event.endpoint, event.token)
    # endregion

    # Commands
    # region EyeSpy commands
    @lightbulb.option("discordid", "Who to follow")
    @lightbulb.command("follow", "Follow a users online status")
    @lightbulb.implements(commands.SlashCommand)
    async def follow(ctx: lightbulb.Context) -> None:
        try:
            req = SpyRequest(spy_user_id=int(ctx.member.id), spy_id=None, spy_target_id=int(ctx.options.discordid))
            target = await ctx.app.rest.fetch_user(req.spy_target_id)
            if ctx.app.manager.add_spy(req):
                requester = await ctx.app.rest.fetch_user(req.spy_user_id)
                await ctx.respond(f"{str(requester)} is now following {str(target)}")
            else:
                await ctx.respond("Unable to follow user, or you are already following them")
        except:
            await ctx.respond("An error occurred while attempting to follow the specified user, make sure the specified ID is correct.")

    @lightbulb.option("discordid", "Who to unfollow")
    @lightbulb.command("unfollow", "Stop following a user")
    @lightbulb.implements(commands.SlashCommand)
    async def unfollow(ctx: lightbulb.Context) -> None:
        try:
            req = SpyRequest(spy_user_id=int(ctx.member.id), spy_id=None, spy_target_id=int(ctx.options.discordid))
            if ctx.app.manager.remove_spy(req):
                requester = await ctx.app.rest.fetch_user(req.spy_user_id)
                target = await ctx.app.rest.fetch_user(req.spy_target_id)
                await ctx.respond(f"{str(requester)} is no longer following {str(target)}")
            else:
                await ctx.respond("Unable to un-follow, or you never previously followed that user")
        except:
            await ctx.respond("An error occurred while attempting to unfollow the specified user, make sure the specified ID is correct.")

    @lightbulb.command("list", "List what users you are following")
    @lightbulb.implements(commands.SlashCommand)
    async def list(ctx: lightbulb.Context) -> None:
        spies = ctx.app.manager.list_spy(int(ctx.member.id))
        if spies == None or len(spies) < 1:
            await ctx.respond(f"It doesn't appear that you are currently following anyone, try `/follow`")
            return

        result = []
        for spy in spies:
            target = await ctx.app.rest.fetch_user(spy)
            result.append((f"{target.username}#{target.discriminator}", spy))

        await ctx.respond(f"You are following: {result}")
    # endregion

    # region Music player commands
    @lightbulb.command("join", "Join your current voice channel")
    @lightbulb.implements(commands.SlashCommand)
    async def join_voice(ctx: lightbulb.Context) -> None:
        await ctx.app.music_manager.join_channel(ctx)

    @lightbulb.command("disconnect", "Disconnect from current voice channel")
    @lightbulb.implements(commands.SlashCommand)
    async def leave_voice(ctx: lightbulb.Context) -> None:
        await ctx.app.music_manager.leave_channel(ctx)

    @lightbulb.option("url", "Track URL")
    @lightbulb.command("play", "Play a song")
    @lightbulb.implements(commands.SlashCommand)
    async def play_song(ctx: lightbulb.Context) -> None:
        await ctx.app.music_manager.play_song(ctx)

    @lightbulb.command("stop", "Stop playing a song")
    @lightbulb.implements(commands.SlashCommand)
    async def stop_song(ctx: lightbulb.Context) -> None:
        await ctx.app.music_manager.stop_song(ctx)
    # endregion
