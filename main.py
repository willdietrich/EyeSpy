import discord
from dotenv import load_dotenv
import logging
import os

load_dotenv()

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

class MyClient(discord.Client):
    async def on_ready(self):
        logger.debug('Logged on as {0}!'.format(self.user), stack_info=True)

    async def on_message(self, message):
        logger.debug('Message from {0.author}: {0.content}'.format(message), stack_info=True)


intents = discord.Intents.default()
intents.presences = True

discord_client_token = os.environ.get('DISCORD_CLIENT_TOKEN')

client = MyClient()
client.run(discord_client_token)
