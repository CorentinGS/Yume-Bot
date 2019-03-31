from discord.ext import commands
import discord
import json

from modules.utils.db import Settings
from modules.utils.format import Embeds


class Games(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.group(aliases=['lg', "ww"])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def werewolf(self, ctx):
        if ctx.invoked_subcommand is None:
            return

    @werewolf.command()
    async def setup(self, ctx):
        set = await Settings().get_games_settings(str(ctx.message.guild.id))
        category = await ctx.guild.create_category_channel("Werewolf")
        set['category'] = str(category.id)
        hub = await ctx.guild.create_voice_channel("Game Hub", user_limit=20, category=category)
        set['hub'] = str(hub.id)

        set['setup'] = True
        await Settings().set_games_settings(str(ctx.message.guild.id), set)

        #TODO: Check if channels are already setup ! 

    @werewolf.command()
    async def start(self, ctx):

        set = await Settings().get_games_settings(str(ctx.message.guild.id))

        if not 'setup' in set:
            set['setup'] = False
            await Settings().set_games_settings(str(ctx.message.guild.id), set)
            return await ctx.send("You must setup your guild before starting the game !\nUse **--werewolf setup**")



        if set['setup'] is False:
            return await ctx.send("You must setup your guild before starting the game !\nUse **--werewolf setup**")

        _hub = int(set["hub"])
        #hub = self.bot.get_channel(_hub)

        hub = discord.utils.get(ctx.guild.voice_channels, id=_hub)

        if hub is None:
            return await ctx.send("You must setup your guild before starting the game !\nUse **--werewolf setup**")

        await ctx.send("Loading...")

    
        if len(hub.members) < 15:
            return await ctx.send("You should be at least 15 to play !")

        #TODO: Ajouter des possibilités à moins que 15 mais virer certains roles ! 

        if len(hub.members) > 20:
            return await ctx.send("You can't be more than 20 !")

        


def setup(bot):
    bot.add_cog(Games(bot))
