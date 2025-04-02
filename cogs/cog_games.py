import discord
from discord import app_commands
from discord.ext import commands
from config import configs

@app_commands.guild_only()
class Games(commands.GroupCog, group_name='games'):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{__name__} loaded')


    @app_commands.command(name='start', description='hangman')
    async def hangman(self, ctx):
        embed = discord.Embed(title="Hangman")
        await ctx.response.send_message(embed=embed)

async def setup(client: commands.Bot):
    await client.add_cog(Games(client), guild=discord.Object(id=configs.get('DEV_GUILD_ID')))
