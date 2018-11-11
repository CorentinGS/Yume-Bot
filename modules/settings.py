import discord
from discord.ext import commands
import datetime
import asyncio

from modules.utils.db import Settings
from modules.utils.format import Embeds

class Set:

    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config



    @commands.group()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def setting(self, ctx):
        if ctx.invoked_subcommand is None:
            # TODO: System d'embed
            return

    @setting.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def muterole(self, ctx, arg: str = None):
        server = str(ctx.guild.id)
        set = await Settings().get_server_settings(server)
        if 'muteRole' not in set:
            set['muteRole'] = False
        elif arg.lower().startswith('on'):
            set['muteRole'] = True
        elif arg.lower().startswith('off'):
            set ['muteRole'] = False
        else:
            return await ctx.send(f'{arg} is not a valid argument ! Please use **ON** or **OFF**')
        await Settings().set_server_settings(server, set)

        await ctx.send('OK !', delete_after=10)



def setup(bot):
    bot.add_cog(Set(bot))
