import discord
import logging
from dotenv import dotenv_values 

class PyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}')
        print(f'Channel List:')
    async def on_message(self, message: discord.Message):
        print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default();
intents.message_content = True
intents.members = True
intents.dm_messages = True
intents.voice_states = True

client = PyClient(intents=intents)
config = dotenv_values(".env")
client.run(config.get("BOT_TOKEN"))
