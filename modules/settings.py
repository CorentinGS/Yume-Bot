import discord
from discord.ext import commands
import datetime
import asyncio

from modules.utils.db import Settings
from modules.utils.format import Embeds

class Settings:

    conf = {}

    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

        global conf
        conf = config


    @commands.group()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def setting(self, ctx):
        if ctx.invoked_subcommand is None:
            return await ctx.send('Please specify something')

    @setting.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, arg: str = None):
        return await ctx.send('LOL')
        # TODO: Choisir le mode de mute et le sauvegarder dans Mongo en boolean. Ensuite il faut ajouter le check des settings dans mod. Il faut aussi faire des embed pour présenter tout ca



def setup(bot):
    bot.add_cog(Settings(bot, bot.config))
