import discord
from dotenv import load_dotenv
from eyespy_client import EyeSpyClient
import os

load_dotenv()
discord_client_token = os.environ.get('DISCORD_CLIENT_TOKEN')

intents = discord.Intents.default()
intents.presences = True
intents.members = True

client = EyeSpyClient(intents=intents)
client.run(discord_client_token)
