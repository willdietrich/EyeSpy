import sqlite3
from time import time
from .decorators.dal_execute import dal_execute
from .decorators.dal_retrieve import dal_retrieve
import discord


class Dal:
    def __init__(self, db: sqlite3.Connection, *args, **kwargs):
        self.db = db
        self.cursor = self.db.cursor()
        self._init_table()

    @dal_execute
    def _init_table(self):
        return 'CREATE TABLE IF NOT EXISTS discord_status (username text NOT NULL, status text, activity text, timestamp integer);'

    @dal_execute
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
        status_insert_sql = f'INSERT INTO discord_status (?, ?, ?, ?) VALUES ({username}, "{str(status)}", "{str(activity)}", {timestamp});'
        return status_insert_sql

    @dal_retrieve
    def get_status(self, ):
        return 'SELECT * FROM discord_status'
