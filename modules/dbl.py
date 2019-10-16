import json

import dbl
from discord.ext import commands, tasks

with open('./config/token.json', 'r') as cjson:
    token = json.load(cjson)

with open('./config/config.json', 'r') as cjson:
    config = json.load(cjson)


class Dbl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.token = token['dbl']
        self.guild = config['support']
        self.debug = config['debug']

        self.dblpy = dbl.DBLClient(self.bot, self.token)

    @tasks.loop(minutes=30.0)
    async def update_stats(self):
        try:
            await self.dblpy.post_guild_count()
        except Exception as e:
            print('Failed to post server count\n{}: {}'.format(type(e).__name__, e))

    @commands.command()
    @commands.is_owner()
    async def dblup(self):
        try:
            await self.dblpy.post_guild_count()
        except Exception as e:
            print('Failed to post server count\n{}: {}'.format(type(e).__name__, e))

def setup(bot):
    bot.add_cog(Dbl(bot))
