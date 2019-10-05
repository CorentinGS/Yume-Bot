import discord
from discord.ext import commands


class Social(commands.Cog):

    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.command()
    async def hug(self, ctx, user: discord.Member = None):
        return

def setup(bot):
    bot.add_cog(Social(bot))