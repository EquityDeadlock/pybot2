import discord
from discord import app_commands
from discord.ext import commands
from config import configs
import random
import nltk
from nltk.corpus import words

@app_commands.guild_only()
class Hangman(commands.GroupCog, group_name='hangman'):
    def __init__(self, client: commands.Bot):
        self.client = client
        nltk.download('words')
        self.word_list = words.words()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{__name__} loaded')


    @app_commands.command(name='start', description='hangman')
    async def hangman_start(self, ctx: discord.Interaction, min: int, max: int):
        word = self.get_random_word(min, max)
        embed = discord.Embed(title="Hangman",description=word)
        await ctx.response.send_message(embed=embed)

    @app_commands.command(name='leaderboard', description='leaderboard')
    async def hangman_leaderboard(self, ctx: discord.Interaction, user: discord.User):
        embed = discord.Embed(title="Hangman Leaderboard",description='')
        await ctx.response.send_message(embed=embed)

    def get_random_word(self, min, max) -> str:
        filtered = [word for word in self.word_list if (len(word) >= min and len(word) <= max)]
        return random.choice(filtered)

async def setup(client: commands.Bot):
    await client.add_cog(Hangman(client), guild=discord.Object(id=configs.get('DEV_GUILD_ID')))
