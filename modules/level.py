import random
from random import randint

import discord
from discord.ext import commands

from modules.utils import checks, lists
from modules.utils.db import Settings


class Level(commands.Cog):

    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.command()
    async def rank(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.message.author

        set = await Settings().get_server_settings(str(ctx.message.guild.id))

        if str(user.id) not in set:

            d = {"level": 0, "xp": 0, "reach": 20}
            set[str(ctx.message.author.id)] = d
            await Settings().set_server_settings(str(ctx.message.guild.id), set)


        dic = set[str(ctx.message.author.id)]
        await ctx.send("{} is level {} | {} / {}".format(user.name, dic['level'], dic["xp"], dic['reach']))


    @commands.Cog.listener()
    async def on_message(self, message):
        user = message.author

        set = await Settings().get_server_settings(str(message.guild.id))
        dic = set[str(user.id)]

        if 'xp' not in dic:
            dic['xp'] = 0
        if 'level' not in dic:
            dic['level'] = 0

        if dic['level'] == 0:
            dic['reach'] = 20

  
        gain = randint(2, 6)

        dic['xp'] += gain
        

        if dic['xp'] >= dic['reach']:
            dic['reach'] = dic['reach'] * 1.5
            dic['xp'] = 0
            dic['level'] += 1

        set[str(user.id)] = dic


        await Settings().set_server_settings(str(message.guild.id), set)


def setup(bot):
    bot.add_cog(Level(bot))