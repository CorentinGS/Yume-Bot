#  Copyright (c) 2020.
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

from typing import Union

import discord
from discord.ext import commands

from modules.sql.blacklistdb import BlacklistDB
from modules.sql.userdb import UserDB
from modules.utils import checks


class Blacklist(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.group(aliases=['bl'])
    @checks.is_owner()
    async def blacklist(self, ctx):
        if ctx.invoked_subcommand is None:
            return

    @blacklist.command()
    @checks.is_owner()
    @commands.guild_only()
    async def add(self, ctx, user: int, reason: str = "None"):

        await ctx.message.delete()
        usery = UserDB.get_one(user)

        if BlacklistDB.is_blacklist(usery):
            return await ctx.send("This user is already blacklisted")
        BlacklistDB.set_blacklist(usery, reason)
        await ctx.send(f"This user is now blacklisted")

    @blacklist.command(aliases=['remove'])
    @checks.is_owner()
    @commands.guild_only()
    async def rm(self, ctx, user: Union[int, discord.Member]):

        if isinstance(user, int):
            user = self.bot.get_user(user)
        await ctx.message.delete()
        usery = UserDB.get_one(user.id)
        if not BlacklistDB.is_blacklist(usery):
            return ctx.send(f"{user.name} is not blacklisted")
        else:
            BlacklistDB.unset_blacklist(usery)
            return await ctx.send("{}#{} is now remove from blacklist".format(user.name, user.discriminator))


def setup(bot):
    bot.add_cog(Blacklist(bot))
