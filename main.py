import os
import sqlite3
from multiprocessing import Process
import uvicorn
from dotenv import load_dotenv
from discordbot.eyespy_client import EyeSpyClient
from dal.dal import Dal


def init_discord_client():
    discord_client_token = os.environ.get('DISCORD_CLIENT_TOKEN')

    client = EyeSpyClient(dal=dal, token=discord_client_token)
    Process.run(client.run())


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
