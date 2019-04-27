import json
import aiohttp
import requests

import discord
from discord.ext import commands

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
    async def init(self, ctx):
        set = await Settings().get_games_settings(str(ctx.message.guild.id))
        set["category"] = None
        await Settings().set_games_settings(str(ctx.message.guild.id), set)

    @werewolf.command()
    async def setup(self, ctx):
        set = await Settings().get_games_settings(str(ctx.message.guild.id))

        if not set['category'] is None:
            cat = set['category']
            try:
                chan = discord.utils.get(ctx.guild.categories, id=int(cat))
                for channel in chan.channels:
                    await channel.delete()
                await chan.delete()
            except discord.Forbidden:
                return await ctx.send("I need more permissions to be able to to that")
            except discord.NotFound:
                pass

        category = await ctx.guild.create_category_channel("Werewolf")
        set['category'] = str(category.id)
        hub = await ctx.guild.create_voice_channel("Game Hub", user_limit=20, category=category)
        set['hub'] = str(hub.id)

        set['setup'] = True
        set['play'] = False
        await Settings().set_games_settings(str(ctx.message.guild.id), set)

    @werewolf.command()
    async def stop(self, ctx):
        set = await Settings().get_games_settings(str(ctx.message.guild.id))
        set['play'] = False
        game = set['game']
        try:
            chan = discord.utils.get(ctx.guild.voice_channels, id=int(game))
            await chan.delete()
        except discord.NotFound:
            pass
        except discord.Forbidden:
            return await ctx.send("I need more permissions to be able to to that")

        await Settings().set_games_settings(str(ctx.message.guild.id), set)

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

        hub = discord.utils.get(ctx.guild.voice_channels, id=_hub)

        if hub is None:
            return await ctx.send("You must setup your guild before starting the game !\nUse **--werewolf setup**")

        if not 'play' in set:
            set['play'] = False

        if set['play'] is True:
            return await ctx.send("A game is already started")

        await ctx.send("Loading...")

        '''
        if len(hub.members) < 15:
            return await ctx.send("You should be at least 15 to play !")

        # TODO: Ajouter des possibilités à moins que 15 mais virer certains roles !

        if len(hub.members) > 20:
            return await ctx.send("You can't be more than 20 !")
        '''

        cat = int(set['category'])
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(connect=False)
        }

        category = discord.utils.get(ctx.guild.categories, id=cat)

        game = await ctx.guild.create_voice_channel("Game Channel", overwrites=overwrites, user_limit=len(hub.members), category=category)

        for user in hub.members:
            await user.move_to(game)

        set['play'] = True
        set['game'] = str(game.id)
        await Settings().set_games_settings(str(ctx.message.guild.id), set)
        await ctx.send("Game is starting")

        data = "{\n\t\"ID\": \"1\",\n\t\"Players\": 20,\n\t\"Host\": 30,\n\t\"Roles\": [\n\t\t1,\n\t\t2,\n\t\t3,\n\t\t4,\n\t\t5,\n\t\t6,\n\t\t7,\n\t\t8,\n\t\t9,\n\t\t10,\n\t\t11,\n\t\t12,\n\t\t13,\n\t\t14,\n\t\t15,\n\t\t16,\n\t\t17,\n\t\t18,\n\t\t19,\n\t\t20\n\t]\n}"
        print(data)
        url = "http://akumu:8080/game/{}".format(ctx.guild.id)

        async with aiohttp.ClientSession() as cs:
            async with cs.post(url, data=data) as r:

                toto = await r.text()
                await ctx.send(toto)

            await cs.close()


    @commands.command()
    async def etefd(self, ctx):
        url = "http://akumu:8080/people/6"

        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                toto = await r.text()
                await ctx.send(toto)


def setup(bot):
    bot.add_cog(Games(bot))
