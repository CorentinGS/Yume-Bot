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

import json

import discord
from discord.ext import commands

from modules.sql.guilddb import GuildDB


class Color(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    with open('modules/guilds/colors.json', 'r') as cjson:
        colors = json.load(cjson)

    @commands.group()
    @commands.guild_only()
    async def color(self, ctx):
        if not ctx.invoked_subcommand:
            return

    @color.command()
    @commands.guild_only()
    async def list(self, ctx):

        await ctx.send("**http://www.html-color-names.com/**")

    '''
    @color.command()
    @checks.is_admin()
    @commands.guild_only()
    async def create(self, ctx, nom: str, hexa: str):
        guild = GuildY(ctx.message.guild)
        await guild.get()
        if not guild.color:
            return await ctx.send("Guild color is not activated")
        if nom in guild.colors:
            return await ctx.send('This name already exists. Please remove it first or use another name.')

        pos = ctx.guild.me.roles[-1].position

        hexa = hexa.lstrip('#')
        r = int(hexa[0:2], 16)
        g = int(hexa[2:4], 16)
        b = int(hexa[4:6], 16)

        color = discord.Colour.from_rgb(r, g, b)

        role = await ctx.guild.create_role(name=nom, colour=color,
                                           reason=f"Color role submitted by {ctx.author.name}|{ctx.author.id}")
        await role.edit(position=pos)

        await ctx.send("Role created", delete_after=3)
        guild.colors[role.name] = role.id
        await guild.set()
    '''

    @color.command()
    @commands.guild_only()
    async def add(self, ctx, name: str):
        guild = GuildDB.get_one(ctx.message.guild.id)

        if not guild.color:
            return

        role = discord.utils.get(ctx.guild.roles, name=name.lower())
        if not role and name.lower() in self.colors:
            pos = ctx.guild.me.roles[-1].position
            hexa = self.colors[name]
            hexa = hexa.lstrip('#')
            r = int(hexa[0:2], 16)
            g = int(hexa[2:4], 16)
            b = int(hexa[4:6], 16)

            color = discord.Colour.from_rgb(r, g, b)
            role = await ctx.guild.create_role(name=name, colour=color,
                                               reason=f"Color role submitted by {ctx.author.name}|{ctx.author.id}")

            await ctx.send("Created : " + role.name)
            await role.edit(position=pos)
        for x in ctx.author.roles:
            if x.name in self.colors:
                await ctx.author.remove_roles(x)
        await ctx.author.add_roles(role)


def setup(bot):
    bot.add_cog(Color(bot))
