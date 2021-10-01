import logging
import discord
from dal.dal import Dal


class EyeSpyClient(discord.Client):
    def __init__(self, dal: Dal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dal = dal
        self.logger = logging.getLogger('discord')
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(filename='./discord.log', encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.logger.addHandler(handler)

    async def on_ready(self):
        self.logger.info('Logged on as {0}!'.format(self.user), stack_info=True)

    async def on_message(self, message):
        self.logger.info('Message from {0.author}: {0.content}'.format(message), stack_info=True)

    async def on_member_update(self, before: discord.member, after: discord.member):
        self.logger.info(f'type: Activity Change, user: {before.name}, status before: {before.raw_status}, status after: {after.raw_status}, activity before: {before.activity}, activity after: {after.activity}')
        self.dal.insert_status(before, after)
