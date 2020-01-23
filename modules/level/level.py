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
from random import randint

import discord
from discord.ext import commands

from modules.sql.guilddb import GuildDB
from modules.sql.rankingsdb import RankingsDB
from modules.sql.userdb import UserDB


class Level(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.command()
    async def rank(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.message.author

        userY = UserDB.get_one(user.id)
        guildY = GuildDB.get_one(ctx.message.guild.id)
        rankings = RankingsDB.get_user(userY, guildY)

        if not rankings:
            RankingsDB.create_ranking(userY, guildY)
            rankings = RankingsDB.get_user(user, guildY)

        rank = RankingsDB.get_rank(userY, guildY)

        em = discord.Embed()
        em.set_author(name=user.name, icon_url=user.avatar_url)
        em.add_field(name="**Rank**", value=f"{rank}", inline=False)
        em.add_field(name="**Level**", value=rankings["level"])
        em.add_field(name="**Progress**",
                     value="{} / {}".format(rankings['xp'], rankings['reach']))
        await ctx.send(embed=em)

    @commands.command(aliases=["scoreboard"])
    async def leaderboard(self, ctx):
        guildY = GuildDB.get_one(ctx.message.guild.id)
        scoreboard = RankingsDB.get_scoreboard(guildY)

        em = discord.Embed(
            description="ScoreBoard",
            color=discord.Colour.magenta()
        )

        x = 0
        for user in scoreboard:
            member = discord.utils.get(ctx.guild.members, id=int(user))
            userY = UserDB.get_one(user)
            member_ranking = RankingsDB.get_user(userY, guildY)
            if member is None:
                RankingsDB.reset_user(userY, guildY)
                continue
            else:
                x += 1
                level = member_ranking['level']
                total = member_ranking['total']
                em.add_field(name=f"**{x} - {member.name}**", value=f"Level : {level} \nTotal xp : {total}",
                             inline=False)

        await ctx.send(embed=em)

    @commands.group()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def level(self, ctx):
        if ctx.invoked_subcommand is None:
            # await ctx.invoke(self.get)
            return

    """
    @level.command()
    @commands.has_permissions(administrator=True)
    async def config(self, ctx, level: int, role: str):

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

        # Create a discord converter to handle both name / mention / ID
    """

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

        userY = UserDB.get_one(user.id)
        guildY = GuildDB.get_one(message.guild.id)
        rankings = RankingsDB.get_user(userY, guildY)

        if not rankings:
            RankingsDB.create_ranking(userY, guildY)
            rankings = RankingsDB.get_user(userY, guildY)

        gain = randint(2, 6)

        rankings['xp'] += gain
        rankings['total'] += rankings['xp']

        if rankings['xp'] >= rankings['reach']:
            rankings['reach'] = round(rankings['reach'] * 1.6)
            rankings['xp'] = 0
            rankings['level'] += 1

            try:
                await message.channel.send("{} is now level {}.".format(user.name, rankings['level']), delete_after=3)
            except discord.Forbidden:
                pass

        RankingsDB.update_user(userY, guildY, rankings)

        """
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
            """


# TODO: Ajouter des commandes pour voir les roles


def setup(bot):
    bot.add_cog(Level(bot))
