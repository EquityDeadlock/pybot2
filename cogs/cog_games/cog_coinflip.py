import nltk
import dcdb
import random
import discord
from config import configs
from discord.ext import commands
from discord import app_commands

@app_commands.guild_only()
class Coinflip(commands.GroupCog, group_name='coinflip'):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{__name__} loaded')

    @app_commands.command(name='once', description='coinflip')
    async def coinflip_once(self, ctx: discord.Interaction):
        result = "Heads" if random.randint(0, 1) else "Tails"
        embed = discord.Embed(description=result)
        await ctx.response.send_message(embed=embed)

async def setup(client: commands.Bot):
    await client.add_cog(Coinflip(client), guild=discord.Object(id=configs.get('DEV_GUILD_ID')))
