import discord
from discord.ext import commands
from config import configs

class Utils(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{__name__} Loaded')

    @discord.app_commands.command(name='ping', description='Pings bot')
    async def sayPing(self, ctx):
        await ctx.response.send_message('Pong!')

async def setup(client: commands.Bot):
    await client.add_cog(Utils(client), guild=discord.Object(id=configs.get('DEV_GUILD_ID')))
