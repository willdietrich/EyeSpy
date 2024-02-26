# import asyncio
import os
import sqlite3

import uvicorn
from dotenv import load_dotenv
from pymongo import MongoClient

from clients import EyeSpyClient
from dal import Dal, AuditDal
from managers import EyeSpyAuditManager, EyeSpyManager


# from multiprocessing import Process
# from alembic.config import Config
# from alembic import command

def init_discord_client():
    discord_client_token = os.getenv('DISCORD_CLIENT_TOKEN')

    client = EyeSpyClient(manager=manager, audit_manager=audit_manager, token=discord_client_token)
    client.run()


def init_api():
    uvicorn.run("api.api:app", host="0.0.0.0", port=8000, log_level="info")


if __name__ == "__main__":
    # Migrate DB settings
    # alembic_cfg = Config("./alembic.ini")
    # command.upgrade(alembic_cfg, "head")

    load_dotenv('../.env')

    # Initialize the spy manager and DAL
    dal = Dal(sqlite3.connect('../db/eyespy.db'))
    manager = EyeSpyManager(dal)

    # Initialize the audit manager and DAL
    mongodb_client = MongoClient(os.getenv('MONGODB_URI'))
    mongodb_db = mongodb_client[os.getenv('MONGODB_DB')]
    mongodb_audit_collection = mongodb_db[os.getenv('MONGODB_AUDIT_COLLECTION')]
    audit_dal = AuditDal(mongodb_client, mongodb_db, mongodb_audit_collection)
    audit_manager = EyeSpyAuditManager(audit_dal)

    # client = Process(target=init_discord_client)
    # client.start()
    init_discord_client()

    # api = Process(target=init_api)
    # api.start()
    # init_api()
