import sqlite3
from time import time
from dal.decorators import dal_execute_param, dal_retrieve
from models import SpyRequest


class Dal:
    def __init__(self, db: sqlite3.Connection, *args, **kwargs):
        self.db = db
        self.cursor = self.db.cursor()

    @dal_execute_param
    def insert_spy(self, request: SpyRequest):
        insert_stmt = 'INSERT INTO DiscordSpys(DiscordId) VALUES (?)'
        insert_data = (request.spy,)

        return insert_stmt, insert_data

    @dal_execute_param
    def insert_target(self, request: SpyRequest):
        insert_stmt = 'INSERT INTO DiscordSpyTargets(DiscordSpyId, DiscordId) VALUES (?, ?)'
        insert_data = (request.spyId, request.spyTarget)

        return insert_stmt, insert_data

    @dal_retrieve
    def get_status(self):
        return 'SELECT * FROM discord_status'
