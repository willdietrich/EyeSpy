import discord
from dotenv import load_dotenv
from discordbot.eyespy_client import EyeSpyClient
import os
import uvicorn


def init_discord_client():
    discord_client_token = os.environ.get('DISCORD_CLIENT_TOKEN')

    intents = discord.Intents.default()
    intents.presences = True
    intents.members = True

    client = EyeSpyClient(intents=intents)
    client.run(discord_client_token)

def init_api():
    uvicorn.run("api.api:app", host="127.0.0.1", port=8000, log_level="info")

if __name__ == "__main__":
    load_dotenv()

    init_discord_client()
    init_api()
