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

        set = await Settings().get_user_settings(str(user.id))

        if 'xp' not in set:
            set['xp'] = 0
        if 'level' not in set:
            set['level'] = 0

        await ctx.send("{} is level {} | {} / {}".format(user.name, set['level'], set['xp'], set['reach']))

    @commands.Cog.listener()
    async def on_message(self, message):
        user = message.author

        set = await Settings().get_user_settings(str(user.id))

        if 'xp' not in set:
            set['xp'] = 0
        if 'level' not in set:
            set['level'] = 0

        if set['level'] == 0:
            set['reach'] = 20

  
        gain = randint(2, 6)

        set['xp'] += gain
        

        if set['xp'] >= set['reach']:
            set['reach'] = set['reach'] * 1.5
            set['xp'] = 0
            set['level'] += 1
        await Settings().set_user_settings(str(user.id), set)




def setup(bot):
    bot.add_cog(Level(bot))