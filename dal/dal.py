import sqlite3
from time import time
from .decorators.dal_execute import dal_execute
from .decorators.dal_retrieve import dal_retrieve
from .decorators.dal_execute_param import dal_execute_param
import discord


class Dal:
    def __init__(self, db: sqlite3.Connection, *args, **kwargs):
        self.db = db
        self.cursor = self.db.cursor()

    @dal_execute_param
    def insert_status(self, before: discord.member, after: discord.member):
        username = before.name
        status = {
            'status_before': before.raw_status,
            'status_after': after.raw_status,
        }
        activity = {
            'activity_before': before.activity,
            'activity_after': after.activity
        }
        timestamp = int(time())
        insert_stmt = 'INSERT INTO discord_status(username, status, activity, timestamp) VALUES (?, ?, ?, ?)'
        insert_data = (username, str(status), str(activity), timestamp)

        return insert_stmt, insert_data

    @dal_retrieve
    def get_status(self, ):
        return 'SELECT * FROM discord_status'
