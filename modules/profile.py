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

#
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#
import discord
from discord.ext import commands


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
    async def ask(self, ctx, user: discord.Member):
        return

def setup(bot):
    bot.add_cog(Profiles(bot))
