import discord
import logging

class EyeSpyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger('discord')
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.logger.addHandler(handler)

    async def on_ready(self):
        self.logger.info('Logged on as {0}!'.format(self.user), stack_info=True)

    async def on_message(self, message):
        self.logger.info('Message from {0.author}: {0.content}'.format(message), stack_info=True)

    async def on_member_update(self, before: discord.member, after: discord.member):
        self.logger.info('user: {0},  before: {1}, after: {2}'.format(before.name, before.activity, after.activity))