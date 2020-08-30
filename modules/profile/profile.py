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
import asyncio

import discord
from discord.ext import commands

from modules.profile.format import Embeds
from model.user import User
from modules.sql.userdb import UserDB


class Profile:
    def __init__(self, user: discord.User):
        # Member
        self.name = [user.name]
        self.id = user.id

        # Profile
        self.gender: str = "Unknown"
        self.age: int = 0
        self.desc: str = 'None'

        # Reputation
        self.rep: int = 0

        # Settings
        self.vip: bool = False

        # Marriage
        self.married: bool = False
        self.lover: int = 0


class Profiles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.guild_only()
    async def marriage(self, ctx):
        if ctx.invoked_subcommand is None:
            return

    @marriage.command()
    @commands.guild_only()
    async def divorce(self, ctx):
        user: User = UserDB.get_one(ctx.author.id)

        if not user.married:
            em = await Embeds.is_not_married(ctx.author)
            await ctx.send(embed=em)
        else:
            loverr: User = UserDB.get_one(user.lover)
            UserDB.unset_lover(user, loverr)

            lover: discord.User = self.bot.get_user(user.lover)
            if not lover:
                return await ctx.send("You're now divorced !")
            em = await Embeds.divorce(ctx.author, lover)
            await ctx.send(embed=em)

    @marriage.command()
    @commands.guild_only()
    async def ask(self, ctx, member: discord.Member):
        user: User = UserDB.get_one(ctx.author.id)
        lover: User = UserDB.get_one(member.id)

        def check(m):
            return m.author == member and m.channel == ctx.channel

        if user.married:
            em = await Embeds.already_married(ctx.author)
            await ctx.send(embed=em)
        elif lover.married:
            em = await Embeds.is_married(member)
            await ctx.send(embed=em)
        else:
            em = await Embeds.ask_to_marry(ctx.author, member)
            await ctx.send(embed=em)
            try:
                message = await self.bot.wait_for('message', check=check, timeout=300)
            except asyncio.TimeoutError:
                await ctx.send("{}, you did not answer quickly enough, if it is an error, repeat the procedure.".format(
                    member.name), delete_after=5)
            else:
                if message.content.lower() == "yes":
                    UserDB.set_lover(ctx.author.id, member.id)
                    em = await Embeds.said_yes(ctx.author, member)
                    await ctx.send(embed=em)
                else:
                    em = await Embeds.said_no(ctx.author, member)
                    await ctx.send(embed=em)

    @marriage.command()
    @commands.guild_only()
    async def get(self, ctx, member: discord.Member = None):
        if not member:
            member: discord.Member = ctx.author
        user: User = UserDB.get_one(member.id)
        if user.married:
            lover: discord.User = self.bot.get_user(int(user.lover))
            if lover:
                em = await Embeds.get_lover(member, lover)
                await ctx.send(embed=em)
            else:
                em = await Embeds.is_married(member)
                await ctx.send(embed=em)
        else:
            em = await Embeds.is_not_married(member)
            await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Profiles(bot))
