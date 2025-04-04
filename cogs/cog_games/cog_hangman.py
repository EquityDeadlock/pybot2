import nltk
import dcdb
import random
import discord
from config import configs
from nltk.corpus import words
from discord.ext import commands
from discord import app_commands

@app_commands.guild_only()
class Hangman(commands.GroupCog, group_name='hangman'):
    def __init__(self, client: commands.Bot):
        self.client = client
        nltk.download('words')
        self.word_list = words.words('en-basic')

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{__name__} loaded')

    @app_commands.command(name='start', description='hangman')
    async def hangman_start(self, ctx: discord.Interaction, min: int, max: int):
        word: str = self.get_random_word(min, max)
        obfuscated: str = Hangman.obfuscate(word)
        formatted = Hangman.embed_format(obfuscated)
        dcdb.Hangman.session_create(word)
        embed = discord.Embed(title=f'Hangman',description=formatted)
        await ctx.response.send_message(embed=embed)

    @app_commands.command(name='leaderboard', description='leaderboard')
    async def hangman_leaderboard(self, ctx: discord.Interaction, user: discord.User):
        embed = discord.Embed(title='Hangman Leaderboard',description='')
        await ctx.response.send_message(embed=embed)

    def get_random_word(self, min, max) -> str:
        filtered = [word for word in self.word_list if (len(word) >= min and len(word) <= max)]
        return random.choice(filtered)

    @app_commands.command(name='games', description='List of current sessions')
    async def hangman_sessions(self, ctx: discord.Interaction):
        sessions = dcdb.Hangman.getSessions()
        embed = discord.Embed(title='Hangman Games',description=sessions)
        await ctx.response.send_message(embed=embed)

    @staticmethod
    def obfuscate(word: str) -> str:
        return '_ ' * len(word)

    @staticmethod
    def embed_format(word: str) -> str:
        return '\\_ ' * word.count('_')

async def setup(client: commands.Bot):
    await client.add_cog(Hangman(client), guild=discord.Object(id=configs.get('DEV_GUILD_ID')))
