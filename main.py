import os
import sqlite3
from multiprocessing import Process

import uvicorn
from dotenv import load_dotenv

from eyespy.clients.eyespy_gateway_client import EyeSpyClient
from eyespy.dal.audit_dal import AuditDal
from eyespy.dal.dal import Dal
from eyespy.dal.mongo_connection import get_mongo_connection
from eyespy.managers.eyespy_audit_manager import EyeSpyAuditManager
from eyespy.managers.eyespy_manager import EyeSpyManager


# from alembic.config import Config
# from alembic import command

def init_discord_client():
    discord_client_token = os.getenv('DISCORD_CLIENT_TOKEN')

    client = EyeSpyClient(manager=manager, audit_manager=audit_manager, token=discord_client_token)
    client.run()


def init_api():
    uvicorn.run("eyespy.api.api:app", host="localhost", port=8000, log_level="info")


if __name__ == "__main__":
    # Migrate DB settings
    # alembic_cfg = Config("./alembic.ini")
    # command.upgrade(alembic_cfg, "head")

    load_dotenv('.env')

    # Initialize the spy manager and DAL
    dal = Dal(sqlite3.connect('db/eyespy.db'))
    manager = EyeSpyManager(dal)

    # Initialize the audit manager and DAL
    connection = get_mongo_connection()
    audit_dal = AuditDal(**connection)
    audit_manager = EyeSpyAuditManager(audit_dal)

    client = Process(target=init_discord_client)
    client.start()
    # init_discord_client()

    api = Process(target=init_api)
    api.start()
    # init_api()
