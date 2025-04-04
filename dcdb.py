import sqlite3
import discord
import os
from enum import IntEnum

DB_NAME = 'sql.db'
TESTING_PRINT_TO_CONSOLE = False 


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
            sqlConnection.commit()
            sqlConnection.close()

def messages_update(before: discord.Message, after: discord.Message):
    try:
        sqlConnection = sqlite3.connect(DB_NAME)
        cursor = sqlConnection.cursor()

        query = '''INSERT OR IGNORE INTO messages (id, guild_id, channel_id, user_id, action, content, reply_id, time) VALUES (?,?,?,?,?,?,?,?);'''
        params = (before.id, before.guild.id, before.channel.id, before.author.id, int(MessageAction.EDIT), before.content, before.reference.message_id if before.reference is not None else None, after.created_at)
        cursor.execute(query, params)
        if TESTING_PRINT_TO_CONSOLE:
            query = '''SELECT * FROM messages;'''
            cursor.execute(query)
            result = cursor.fetchall()
            print(result)
    except sqlite3.Error as error:
        print(f'Error: {error}')
    finally:
        sqlConnection.commit()
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
        sqlConnection.commit()
        sqlConnection.close()

class Hangman:
    game_id = 1
    @staticmethod
    def session_create(word: str):
        try:
            sqlConnection = sqlite3.connect(DB_NAME)
            cursor = sqlConnection.cursor()

            query = '''INSERT OR IGNORE INTO hangman_sessions (id, word, winner) VALUES (?,?,?);'''
            params = (Hangman.game_id, word, None)

            cursor.execute(query, params)
        except sqlite3.Error as error:
            print(f'Error: {error}')
        finally:
            sqlConnection.commit()
            sqlConnection.close()
            Hangman.game_id += 1

    @staticmethod
    def session_update_winner(id: int, winner: discord.User.id):
        try:
            sqlConnection = sqlite3.connect(DB_NAME)
            cursor = sqlConnection.cursor()

            query = '''UPDATE hangman_sessions SET winner=? WHERE id=?;'''
            params = (winner, id)

            cursor.execute(query, params)
        except sqlite3.Error as error:
            print(f'Error: {error}')
        finally:
            sqlConnection.commit()
            sqlConnection.close()

    @staticmethod
    def getSessions():
        try:
            sqlConnection = sqlite3.connect(DB_NAME)
            cursor = sqlConnection.cursor()

            query = '''SELECT id, word FROM hangman_sessions;'''

            cursor.execute(query)

            result = cursor.fetchmany(size=5)
        except sqlite3.Error as error:
            print(f'Error: {error}')
        finally:
            sqlConnection.commit()
            sqlConnection.close()
            return result

    @staticmethod
    def session_update(id: int, word: str, winner: discord.User.id):
        try:
            sqlConnection = sqlConnection.connect(DB_NAME)
            cursor = sqlConnection.cursor()

            query = '''INSERT INTO OR IGNORE hangman_sessions (id, word, winner) VALUES (?,?,?);'''
            params = (game_id, word, winner)

            cursor.execute(query, params)
        except sqlite3.Error as error:
            print(f'Error: {error}')
        finally:
            sqlConnection.commit()
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

        query = '''CREATE TABLE IF NOT EXISTS hangman_sessions(
                id INTEGER NOT NULL,
                word TEXT NOT NULL,
                winner INTEGER,
                PRIMARY KEY(id, word));
            '''
        cursor.execute(query)

        query = '''CREATE TABLE IF NOT EXISTS hangman_guesses(
                id INTEGER NOT NULL,
                session_id ID NOT NULL,
                user INTEGER NOT NULL,
                type INTEGER NOT NULL,
                guess TEXT NOT NULL,
                PRIMARY KEY(id, session_id, user, type, guess));'''
        cursor.execute(query)


        if TESTING_PRINT_TO_CONSOLE:
            query = '''Select * from guilds;'''
            cursor.execute(query)
            result = cursor.fetchmany(size=5)
            print(result)
            query = '''Select * from users;'''
            cursor.execute(query)
            result = cursor.fetchmany(size=5)
            print(result)
            query = '''Select * from levels;'''
            cursor.execute(query)
            result = cursor.fetchmany(size=5)
            print(result)
            query = '''Select * from messages;'''
            cursor.execute(query)
            result = cursor.fetchmany(size=5)
            print(result)

    except sqlite3.Error as error:
        print(f'Error: {error}')
    finally:
        sqlConnection.commit()
        sqlConnection.close()

def db_delete():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)

class MessageAction(IntEnum):
    CREATE = 1
    EDIT = 2
    REPLY = 3
    DELETE = 4
