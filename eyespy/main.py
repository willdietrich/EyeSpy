# import asyncio
import os
import sqlite3

# from multiprocessing import Process
import uvicorn
from dotenv import load_dotenv

from .clients import EyeSpyClient
from .dal import Dal
from .managers import EyeSpyManager

# from alembic.config import Config
# from alembic import command


def init_discord_client():
    discord_client_token = os.environ.get('DISCORD_CLIENT_TOKEN')

    client = EyeSpyClient(manager=manager, token=discord_client_token)
    client.run()


def init_api():
    uvicorn.run("api.api:app", host="0.0.0.0", port=8000, log_level="info")


if __name__ == "__main__":
    load_dotenv()

    # Migrate DB settings
    #alembic_cfg = Config("./alembic.ini")
    #command.upgrade(alembic_cfg, "head")

    dal = Dal(sqlite3.connect('./db/eyespy.db'))
    manager = EyeSpyManager(dal)

    # client = Process(target=init_discord_client)
    # client.start()

    init_discord_client()

    # api = Process(target=init_api)
    # api.start()