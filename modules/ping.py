import discord
from discord.ext import commands
import json


class Ping:

    conf = {}

    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

        global conf
        conf = config

    @commands.command(pass_context=True)
    @commands.guild_only()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def ping(self, ctx):

        return await ctx.send("Pong !!")

    @commands.command(pass_context=True)
    @commands.guild_only()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def pong(self, ctx):

        return await ctx.send("Ping !!")


def setup(bot):
    bot.add_cog(Ping(bot, bot.config))
