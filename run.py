import discord
from discord.ext import commands
import logging
import signal
import os
import sys
import sqlite3
import dcdb
from config import configs

TESTING_PRINT_TO_CONSOLE = True

def signal_handler(sig, frame):
    if TESTING_PRINT_TO_CONSOLE:
        print(f'Signal Recieved: {sig}')
        dcdb.db_delete()
    else:
        if TESTING_PRINT_TO_CONSOLE:
            print('failed to destroy database')
    sys.exit(0)

class PyClient(commands.Bot):
    async def setup_hook(self):
        loaded_count = await load(configs.get('DIR_COGS'))
        print(f'Loaded: {loaded_count}')
        try:
            guild = discord.Object(id=configs.get('DEV_GUILD_ID'))
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} commands to guild [{guild.id}]')
        except Exception as e:
            print(f'Failed to sync: {e}')

    async def on_ready(self):
        print(f'Logged on as {self.user}')
        for guild in self.guilds:
            dcdb.guilds_create(guild)

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

client = PyClient(command_prefix=";", intents=intents)

async def load(dir: str, count: int = 0) -> int:
    print('Loading cogs:')
    for file in os.listdir(dir):
        if file.startswith('cog_') and file.endswith('.py'):
            await client.load_extension(f'{dir.replace("/", ".")}.{file[:-3]}')
            print(f'Cog: {file[:-3]}')
            count += 1
        elif file.startswith('cog_'):
            count = await load(dir + '/' + file, count)
        else:
            pass
    return count

client.run(configs.get("BOT_TOKEN"))
