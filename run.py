import discord
from discord.ext import commands
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

class PyClient(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}')
        try:
            guild = discord.Object(id=config.get('DEV_GUILD_ID'))
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} commands to guild [{guild.id}]')
        except Exception as e:
            print(f'Failed to sync: {e}')
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

config = dotenv_values(".env")
dcdb.sql_init_schema()

intents = discord.Intents.default();
intents.message_content = True
intents.members = True
intents.dm_messages = True
intents.voice_states = True
intents.guilds = True

client = PyClient(command_prefix=";", intents=intents)

@client.tree.command(name='ping', description='Pings bot', guild=discord.Object(id=config.get("DEV_GUILD_ID")))
async def sayPing(interaction: discord.Interaction):
    await interaction.response.send_message('Pong!')

client.run(config.get("BOT_TOKEN"))
