import logging

import hikari
import lavasnek_rs
import lightbulb


class EventHandler:
    """Events from the Lavalink server"""

    async def track_start(self, _: lavasnek_rs.Lavalink, event: lavasnek_rs.TrackStart) -> None:
        logging.info("Track started on guild: %s", event.guild_id)

    async def track_finish(self, _: lavasnek_rs.Lavalink, event: lavasnek_rs.TrackFinish) -> None:
        logging.info("Track finished on guild: %s", event.guild_id)

    async def track_exception(self, lavalink: lavasnek_rs.Lavalink, event: lavasnek_rs.TrackException) -> None:
        logging.warning("Track exception event happened on guild: %d", event.guild_id)

        # If a track was unable to be played, skip it
        skip = await lavalink.skip(event.guild_id)
        node = await lavalink.get_guild_node(event.guild_id)

        if not node:
            return

        if skip and not node.queue and not node.now_playing:
            await lavalink.stop(event.guild_id)

class MusicManager:

    def __init__(self):
        self.lavalink: lavasnek_rs.Lavalink = None
        self.track_handle = None

    async def start_lavalink(self, event: hikari.ShardReadyEvent, token: str) -> None:
        """Event that triggers when the hikari gateway is ready."""

        builder = (
            # TOKEN can be an empty string if you don't want to use lavasnek's discord gateway.
            lavasnek_rs.LavalinkBuilder(event.my_user.id, token)
                # This is the default value, so this is redundant, but it's here to show how to set a custom one.
                .set_host("127.0.0.1").set_password("youshallnotpass")
        )

        builder.set_start_gateway(False)

        # lava_client = await builder.build(EventHandler())
        lava_client = await builder.build(EventHandler())

        self.lavalink = lava_client

    async def join_voice_channel(self, ctx: lightbulb.Context):
        # Get the guild ID of the command context
        guild_id = ctx.guild_id

        # Get the user's voice state in the guild
        guild = await ctx.bot.rest.fetch_guild(guild_id)

        voice_state = guild.get_voice_state(ctx.author.id)

        # Check if the user is in a voice channel
        if not voice_state or not voice_state.channel_id:
            await ctx.respond("You need to join a voice channel first.")
            return None

        # Get the voice channel object from the channel ID
        voice_channel = await ctx.bot.rest.fetch_channel(voice_state.channel_id)

        if not voice_channel:
            await ctx.respond(f"Unable to connect to voice channel: {voice_channel.name}")
            return

        await ctx.app.update_voice_state(ctx.guild_id, voice_state.channel_id, self_deaf=True)
        connection_info = await self.lavalink.wait_for_full_connection_info_insert(ctx.guild_id)

        await self.lavalink.create_session(connection_info)

        await ctx.respond(f"Joined voice channel: {voice_channel.name}")

    async def join_channel(self, ctx: lightbulb.Context):
        await self.join_voice_channel(ctx)

    async def leave_channel(self, ctx: lightbulb.Context):
        await self.lavalink.destroy(ctx.guild_id)

        if ctx.guild_id is not None:
            await ctx.app.update_voice_state(ctx.guild_id, None)
            await self.lavalink.wait_for_connection_info_remove(ctx.guild_id)

        # Destroy nor leave remove the node nor the queue loop, you should do this manually.
        await self.lavalink.remove_guild_node(ctx.guild_id)
        await self.lavalink.remove_guild_from_loops(ctx.guild_id)

        await ctx.respond("Left voice channel")

    # async def play_song(self, ctx: lightbulb.Context) -> str:
