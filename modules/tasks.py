from itertools import cycle

import discord
from discord.ext import commands, tasks


class Tasks(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    # self.chng_pr.start()

    @tasks.loop(seconds=30.0)
    async def chng_pr(self):
        status = ['--help', 'Peace and Dream', 'By YumeNetwork']
        status = cycle(status)

        name = next(status)
        await self.bot.change_presence(activity=discord.Game(name=name))

    @chng_pr.before_loop
    async def wait_for_bot(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Tasks(bot))
