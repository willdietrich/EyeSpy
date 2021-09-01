import logging
import discord
import sqlite3
from time import time


class EyeSpyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        create_table_sql = 'CREATE TABLE IF NOT EXISTS discord_status (username text NOT NULL, status_before text, status_after text, activity_before text, activity_after text, timestamp integer);'

        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger('discord')
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(filename='./discord.log', encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.logger.addHandler(handler)
        self.db = sqlite3.connect('discord.db')
        cursor = self.db.cursor()
        cursor.execute(create_table_sql) 
        self.db.commit()

    async def on_ready(self):
        self.logger.info('Logged on as {0}!'.format(self.user), stack_info=True)

    async def on_message(self, message):
        self.logger.info('Message from {0.author}: {0.content}'.format(message), stack_info=True)

    async def on_member_update(self, before: discord.member, after: discord.member):
        if before.activity == None:
            self.logger.info(f'type: Status Change, user: {before.name}, status before: {before.raw_status}, status after: {after.raw_status}')
        else:
            self.logger.info(f'type: Activity Change, user: {before.name}, status before: {before.raw_status}, status after: {after.raw_status}, activity before: {before.activity}, activity after: {after.activity}')

        status = {
            'username': before.name,
            'status_before': before.raw_status,
            'status_after': after.raw_status,
            'timestamp': int(time())
        }
        activity = {
            'username': before.name,
            'status_before': before.raw_status,
            'status_after': after.raw_status,
            'timestamp': int(time()),
            'activity_before': before.activity,
            'activity_after': after.activity
        }

        if before.activity == None:
            values = status
        else:
            values = activity
        
        for k,v in values.items():
            values[k] = str(v)
        
        joiner = '", "'
        #print(f'Keys: {list(values.keys())}\nValues: {list(values.values())}')
        status_insert_sql = f'INSERT INTO discord_status ({",".join(list(values.keys()))}) VALUES ( "{joiner.join(list(values.values()))}" )'
        #self.logger.info(status_insert_sql)
        #print(status_insert_sql)
        select_sql = 'SELECT * FROM discord_status'
        cursor = self.db.cursor()
        cursor.execute(status_insert_sql)
        self.db.commit()
        
        '''
        cursor.execute(select_sql)
        print(f'{cursor.fetchall()}\n')
        '''