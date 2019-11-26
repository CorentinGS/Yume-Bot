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
import collections
from random import randint

import discord
from discord.ext import commands

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

        ranks = {}
        set = await Settings().get_user_settings(str(ctx.message.guild.id))

        if str(user.id) not in set:
            d = {"level": 0, "xp": 0, "reach": 20, "total": 0}
            set[str(user.id)] = d
            await Settings().set_user_settings(str(ctx.message.guild.id), set)

        for id in set.keys():
            if id == '_id':
                continue
            toto = set[str(id)]
            ranks[id] = toto["total"]

        sorted_x = sorted(ranks.items(), key=lambda kv: kv[1], reverse=True)
        sorted_dict = collections.OrderedDict(sorted_x).copy()
        print(sorted_dict)
        rank = list(sorted_dict.keys()).index(str(user.id))

        dic = set[str(user.id)]
        em = discord.Embed()
        em.set_author(name=user.name, icon_url=user.avatar_url)
        em.add_field(name="**Rank**", value=str(rank + 1), inline=False)
        em.add_field(name="**Level**", value=dic["level"])
        em.add_field(name="**Progress**",
                     value="{} / {}".format(dic['xp'], dic['reach']))
        await ctx.send(embed=em)

    @commands.command(aliases=["scoreboard"])
    async def leaderboard(self, ctx):
        set = await Settings().get_user_settings(str(ctx.message.guild.id))
        ranks = {}
        x = 0
        em = discord.Embed(
            description="ScoreBoard",
            color=discord.Colour.magenta()
        )

        for user in set.keys():
            if user == '_id':
                continue
            toto = set[str(user)]
            ranks[user] = toto["total"]

        sorted_x = sorted(ranks.items(), key=lambda kv: kv[1], reverse=True)
        sorted_dict = collections.OrderedDict(sorted_x).copy()
        for user in sorted_dict.keys():
            member = discord.utils.get(ctx.guild.members, id=int(user))
            if member is None:
                # del sorted_dict[user]
                continue
            else:
                x += 1
                level = set[str(user)]['level']
                total = set[str(user)]['total']
                em.add_field(name=f"**{x} - {member.name}**", value=f"Level : {level} \nTotal xp : {total}",
                             inline=False)

                if x == 10:
                    break

        await ctx.send(embed=em)

    @commands.group()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def level(self, ctx):
        if ctx.invoked_subcommand is None:
            # await ctx.invoke(self.get)
            return

    @level.command()
    @commands.has_permissions(administrator=True)
    async def config(self, ctx, level: int, role: str):
        """
        Config the auto role
        """
        set = await Settings().get_server_settings(str(ctx.message.guild.id))

        if not "levels" in set:
            set["levels"] = {}
        await Settings().set_server_settings(str(ctx.message.guild.id), set)
        try:
            rolemention = discord.utils.get(ctx.guild.roles, name=role)
        except discord.NotFound:
            return await ctx.send(
                "We can't find the role. Be sure to follow the syntax as in the exemple : **--level set 3 test_role**")
        except discord.InvalidArgument:
            return await ctx.send(
                "We can't find the role. Be sure to follow the syntax as in the exemple : **--level set 3 test_role**")

        toto = set["levels"]
        toto[str(level)] = str(rolemention.id)
        set["levels"] = toto

        await Settings().set_server_settings(str(ctx.message.guild.id), set)
        await ctx.send("Level setup")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """

        :param message: The message that has been sent
        """
        user = message.author

        if user.bot is True or message.guild is None:
            return

        if message.guild.id == '264445053596991498':
            return

        set = await Settings().get_user_settings(str(message.guild.id))
        toto = await Settings().get_server_settings(str(message.guild.id))

        if not str(user.id) in set:
            d = {"level": 0, "xp": 0, "reach": 20, "total": 0}
            set[str(user.id)] = d

        if "levels" not in toto:
            toto["levels"] = {}

        await Settings().set_user_settings(str(message.guild.id), set)

        dic = set[str(user.id)]
        gain = randint(2, 5)

        dic['xp'] += gain
        dic['total'] += dic['xp']

        if dic['xp'] >= dic['reach']:
            dic['reach'] = round(dic['reach'] * 1.6)
            dic['xp'] = 0
            dic['level'] += 1

            lvl = toto["levels"]
            for key in lvl:
                if int(key) == dic['level']:
                    try:
                        role = discord.utils.get(
                            message.guild.roles, id=int(lvl[key]))
                    except discord.NotFound:
                        break
                    try:
                        await user.add_roles(role)
                    except discord.Forbidden:
                        break
                    except discord.InvalidArgument:
                        break

            try:
                await message.channel.send("{} is now level {}.".format(user.name, dic['level']), delete_after=3)
            except discord.Forbidden:
                pass

        set[str(user.id)] = dic
        await Settings().set_user_settings(str(message.guild.id), set)


# TODO: Ajouter des commandes pour voir les roles


def setup(bot):
    bot.add_cog(Level(bot))
