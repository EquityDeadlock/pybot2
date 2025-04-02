import discord
from discord import app_commands
from discord.ext import commands
from config import configs

@app_commands.guild_only()
class Level(commands.GroupCog, group_name='level'):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{__name__} loaded')


    @app_commands.command(name='check', description='Check your level')
    async def level_check(self, ctx):
        embed = discord.Embed(title="Level: 0")
        await ctx.response.send_message(embed=embed)

async def setup(client: commands.Bot):
    await client.add_cog(Level(client), guild=discord.Object(id=configs.get('DEV_GUILD_ID')))
