import os
import sqlite3

# from multiprocessing import Process
import uvicorn
from dotenv import load_dotenv

from clients import EyeSpyClient, DiscordRestClient
from dal import Dal


def init_discord_client():
    discord_client_token = os.environ.get('DISCORD_CLIENT_TOKEN')

    rest_client = DiscordRestClient(token=discord_client_token)
    client = EyeSpyClient(dal=dal, rest_client=rest_client, token=discord_client_token)
    client.run()


def init_api():
    uvicorn.run("api.api:app", host="127.0.0.1", port=8000, log_level="info")


if __name__ == "__main__":
    load_dotenv()

    dal = Dal(sqlite3.connect('eyespy.db'))

    # client = Process(target=init_discord_client)
    # client.start()
    init_discord_client()

    # api = Process(target=init_api)
    # api.start()
