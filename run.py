import discord
import logging
import signal
import sys
import os
import sqlite3
from enum import IntEnum
from dotenv import dotenv_values

TESTING_PRINT_TO_CONSOLE = True

def signal_handler(sig, frame):
    if TESTING_PRINT_TO_CONSOLE:
        print(f'Signal Recieved: {sig}')
    if os.path.exists("sql.db"):
        os.remove("sql.db")
    else:
        if TESTING_PRINT_TO_CONSOLE:
            print('failed to destroy database')
    sys.exit(0)

class MessageAction(IntEnum):
    CREATE = 1
    EDIT = 2
    REPLY = 3
    DELETE = 4

class PyClient(discord.Client):
    async def on_ready(self):
        try:
            sqlConnection = sqlite3.connect('sql.db')
            cursor = sqlConnection.cursor()
            for guild in self.guilds:
                print(guild.name)
                query = '''INSERT OR IGNORE INTO guilds (id, name, shard_id, chunked, member_count) VALUES (?,?,?,?,?);'''
                params = (guild.id, guild.name, guild.shard_id, 1 if guild.chunked else 0, guild.member_count)
                cursor.execute(query, params)
            if TESTING_PRINT_TO_CONSOLE:
                query = '''SELECT * FROM guilds;'''
                cursor.execute(query)
                result = cursor.fetchall()
                print(result)
        except sqlite3.Error as error:
            print(f'Error: {error}')
        finally:
            sqlConnection.close()
        print(f'Logged on as {self.user}')
        print(f'Channel List:')

    async def on_message(self, message: discord.Message):
        print(f'Message from guild: [{message.guild.id},{message.guild.name}] - {message.author}: {message.content}')
        if isinstance(message, discord.channel.DMChannel):
            return
        try:
            sqlConnection = sqlite3.connect('sql.db')
            cursor = sqlConnection.cursor()

            query = '''INSERT OR IGNORE INTO messages (id, guild_id, channel_id, user_id, action, content, reply_id, time) VALUES (?,?,?,?,?,?,?,?);'''
            params = (message.id, message.guild.id, message.channel.id, message.author.id, int(MessageAction.REPLY) if message.reference is not None else int(MessageAction.CREATE), message.content, message.to_reference().message_id if message.reference is not None else None, message.created_at)
            cursor.execute(query, params)
            if TESTING_PRINT_TO_CONSOLE:
                query = '''SELECT * FROM messages;'''
                cursor.execute(query)
                result = cursor.fetchall()
                print(result)
        except sqlite3.Error as error:
            print(f'Error: {error}')
        finally:
            sqlConnection.close()


        print(f'Message from guild: [{message.guild.id},{message.guild.name}] - {message.author}: {message.content}')

def sql_init_schema():
    try:
        sqlConnection = sqlite3.connect("sql.db")
        cursor = sqlConnection.cursor()

        query = '''CREATE TABLE IF NOT EXISTS guilds(
                    id INTEGER NOT NULL PRIMARY KEY,
                    name TEXT NOT NULL,
                    shard_id INTEGER NOT NULL,
                    chunked INTEGER NOT NULL,
                    member_count INTEGER NOT NULL);'''
        cursor.execute(query)

        query = '''CREATE TABLE IF NOT EXISTS users(
                id INTEGER NOT NULL PRIMARY KEY,
                guild_id INTEGER NOT NULL,
                name TEXT NOT NULL);'''
        cursor.execute(query)

        query = '''CREATE TABLE IF NOT EXISTS messages(
                id INTEGER NOT NULL,
                guild_id INTEGER NOT NULL,
                channel_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                action INTEGER NOT NULL,
                content BLOB NOT NULL,
                reply_id INTEGER,
                time BLOB NOT NULL,
                PRIMARY KEY(id, guild_id, channel_id, user_id));
            '''
        cursor.execute(query)

        query = '''CREATE TABLE IF NOT EXISTS levels(
                guild_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                PRIMARY KEY(guild_id, user_id));
            '''
        cursor.execute(query)

        query = '''Select * from guilds,users,levels;'''
        cursor.execute(query)
        result = cursor.fetchall()
        print(result)

        cursor.close()

    except sqlite3.Error as error:
        print(f'Error: {error}')
    finally:
        sqlConnection.close()


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

sql_init_schema()

intents = discord.Intents.default();
intents.message_content = True
intents.members = True
intents.dm_messages = True
intents.voice_states = True
intents.guilds = True


client = PyClient(intents=intents)
config = dotenv_values(".env")
client.run(config.get("BOT_TOKEN"))
