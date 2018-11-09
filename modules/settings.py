import discord
from discord.ext import commands
import datetime
import asyncio

from modules.utils.db import Settings
from modules.utils.format import Embeds

class Set:

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
            return

    @setting.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def muterole(self, ctx, arg: str = None):
        server = str(ctx.guild.id)
        set = await Settings().get_server_settings(server)
        if 'muteRole' not in set:
            set['muteRole'] = False
        if arg == "On":
            set['muteRole'] = True
        elif arg == "Off":
            set ['muteRole'] = False
        else:
            return await ctx.send(f'{arg} is not a valid argument ! Please use **On** or **Off**')
        await Settings().set_server_settings(server, set)

        return await ctx.send('LOL')
        # TODO: Choisir le mode de mute et le sauvegarder dans Mongo en boolean. Ensuite il faut ajouter le check des settings dans mod. Il faut aussi faire des embed pour présenter tout ca



def setup(bot):
    bot.add_cog(Set(bot, bot.config))
