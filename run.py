import discord
import logging
import signal
import sys
import sqlite3
import dcdb
from dotenv import dotenv_values

TESTING_PRINT_TO_CONSOLE = True

def signal_handler(sig, frame):
    if TESTING_PRINT_TO_CONSOLE:
        print(f'Signal Recieved: {sig}')
        dcdb.db_delete()
    else:
        if TESTING_PRINT_TO_CONSOLE:
            print('failed to destroy database')
    sys.exit(0)

class PyClient(discord.Client):
    async def on_ready(self):
        for guild in self.guilds:
            dcdb.guilds_create(guild)
        print(f'Logged on as {self.user}')

    async def on_message(self, message: discord.Message):
        if isinstance(message, discord.channel.DMChannel):
            print(f'DM Message from {message.author}: {message.content}')
            return
        dcdb.messages_create(message)
        print(f'Message in guild: [{message.guild.id},{message.guild.name}] - {message.author}: "{message.content}"')
    
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if isinstance(before, discord.channel.DMChannel):
            print(f'DM Message Edit {before.author}: "{before.content}" - "{after.content}"')
            return
        dcdb.messages_update(before, after)
        print(f'Message in guild: [{before.guild.id},{before.guild.name}] - {before.author}: "{before.content}" - "{after.content}"')

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

dcdb.sql_init_schema()

intents = discord.Intents.default();
intents.message_content = True
intents.members = True
intents.dm_messages = True
intents.voice_states = True
intents.guilds = True

client = PyClient(intents=intents)
config = dotenv_values(".env")
client.run(config.get("BOT_TOKEN"))
