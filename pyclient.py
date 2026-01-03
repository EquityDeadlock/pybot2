import os
import dcdb
import discord
from discord.ext import commands
from config import configs


class PyClient(commands.Bot):
    async def load(self, dir: str, count: int = 0) -> int:
        if(self.firstCog):
            self.firstCog = False
            print('Loading cogs:')
        for file in os.listdir(dir):
            if file.startswith('cog_') and file.endswith('.py'):
                await self.load_extension(f'{dir.replace("/", ".")}.{file[:-3]}')
                print(f'Cog: {file[:-3]}')
                count += 1
            elif file.startswith('cog_'):
                count = await self.load(dir + '/' + file, count)
            else:
                pass
        return count

    async def setup_hook(self):
        self.firstCog = True
        self.loaded_cogs = await self.load(configs.get('DIR_COGS'))
        print(f'Loaded: {self.loaded_cogs}')
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
