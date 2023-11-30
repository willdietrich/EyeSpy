import sqlite3
from time import time
from .decorators import dal_execute, dal_retrieve
from models import SpyRequest, NotifySpyRequest


class Dal:
    def __init__(self, db: sqlite3.Connection, *args, **kwargs):
        self.db = db
        self.cursor = self.db.cursor()

    @dal_execute
    def insert_spy(self, request: SpyRequest):
        insert_stmt = 'INSERT INTO DiscordSpys(DiscordId) VALUES (?)'
        insert_data = (request.spy_user_id,)

        return insert_stmt, insert_data

    @dal_execute
    def insert_target(self, request: SpyRequest):
        insert_stmt = 'INSERT INTO DiscordSpyTargets(DiscordSpyId, DiscordId) VALUES (?, ?)'
        insert_data = (request.spy_id, request.spy_target_id)

        return insert_stmt, insert_data

    @dal_execute
    def delete_target(self, request: SpyRequest):
        delete_stmt = 'DELETE FROM DiscordSpyTargets  WHERE DiscordSpyId=? AND DiscordId=?'
        delete_data = (request.spy_id, request.spy_target_id)

        return delete_stmt, delete_data

    @dal_retrieve
    def check_target_exists(self, request: SpyRequest):
        stmt = 'SELECT s.DiscordSpyId as spy FROM DiscordSpys s JOIN DiscordSpyTargets t ON s.DiscordSpyId = t.DiscordSpyId WHERE s.DiscordId=? AND t.DiscordId=?'
        data = (request.spy_user_id, request.spy_target_id)

        return stmt, data

    @dal_retrieve
    def get_spy_id(self, request: SpyRequest):
        stmt = 'SELECT s.DiscordSpyId as spy FROM DiscordSpys s WHERE s.DiscordId=?'
        data = (request.spy_user_id,)

        return stmt, data

    @dal_retrieve
    def get_spies(self, request: NotifySpyRequest):
        stmt = 'SELECT s.DiscordId as spy FROM DiscordSpys s JOIN DiscordSpyTargets t ON s.DiscordSpyId = t.DiscordSpyId WHERE t.DiscordId=?'
        data = (request.status_change_user_id,)
        return stmt, data

    @dal_retrieve
    def get_spies_for_user(self, user: int):
        stmt = 'SELECT t.DiscordId as spy FROM DiscordSpys s JOIN DiscordSpyTargets t ON s.DiscordSpyId = t.DiscordSpyId WHERE s.DiscordId=?'
        data = (user,)

        return stmt, data
