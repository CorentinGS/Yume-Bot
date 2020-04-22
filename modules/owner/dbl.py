#  Copyright (c) 2019.
#  MIT License
#
#  Copyright (c) 2019 YumeNetwork
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.


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
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True)

    """
    @tasks.loop(minutes=45.0)
    async def update_stats(self):
        if not self.bot.id == 456504213262827524:
            return
        try:
            await self.dblpy.post_guild_count()
            print('DBL updated')
        except Exception as e:
            print('Failed to post server count\n{}: {}'.format(type(e).__name__, e))
    """
    
    @commands.Cog.listener()
    async def on_guild_post(self):
        print("Server count posted successfully")

    @commands.command()
    @commands.is_owner()
    async def dblup(self, ctx):
        try:
            await self.dblpy.post_guild_count()
            print('DBL updated')
            await ctx.send("DBL updated")
        except Exception as e:
            print('Failed to post server count\n{}: {}'.format(type(e).__name__, e))
            await ctx.send("Error : \n`{}`".format(e))

def setup(bot):
    bot.add_cog(Dbl(bot))
