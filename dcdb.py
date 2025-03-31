import sqlite3
import discord
import os
from enum import IntEnum

DB_NAME = 'sql.db'
TESTING_PRINT_TO_CONSOLE = True


def messages_create(message: discord.Message):
    try:
        sqlConnection = sqlite3.connect(DB_NAME)
        cursor = sqlConnection.cursor()

        query = '''INSERT OR IGNORE INTO messages (id, guild_id, channel_id, user_id, action, content, reply_id, time) VALUES (?,?,?,?,?,?,?,?);'''
        params = (message.id, message.guild.id, message.channel.id, message.author.id, int(MessageAction.REPLY) if message.reference is not None else int(MessageAction.CREATE), message.content, message.reference.message_id if message.reference is not None else None, message.created_at)
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

def messages_update(before: discord.Message, after: discord.Message):
    try:
        sqlConnection = sqlite3.connect(DB_NAME)
        cursor = sqlConnection.cursor()

        query = '''INSERT OR IGNORE INTO messages (id, guild_id, channel_id, user_id, action, content, reply_id, time) VALUES (?,?,?,?,?,?,?,?);'''
        params = (before.id, before.guild.id, before.channel.id, before.author.id, int(MessageAction.EDIT), before.content, before.reference.message_id if before.reference is not None else None, before.created_at)
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

def guilds_create(guild: discord.Guild):
    try:
        sqlConnection = sqlite3.connect(DB_NAME)
        cursor = sqlConnection.cursor()
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


def sql_init_schema():
    try:
        sqlConnection = sqlite3.connect(DB_NAME)
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

def db_delete():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)

class MessageAction(IntEnum):
    CREATE = 1
    EDIT = 2
    REPLY = 3
    DELETE = 4
