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

import typing
from random import randint

import discord
from discord.ext import commands
from modules.utils import checks, lists

from modules.sql.guilddb import GuildDB
from modules.sql.rankingsdb import RankingsDB
from modules.sql.roledb import RoleDB
from modules.sql.userdb import UserDB


class Level(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config
        self._cd = commands.CooldownMapping.from_cooldown(
            1.0, 5.0, commands.BucketType.user)

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

    @level.command()
    @commands.has_permissions(administrator=True)
    async def config(self, ctx, level: int, role: typing.Union[discord.Role, int, str]):
        guild = GuildDB.get_one(ctx.guild.id)
        if isinstance(role, str):
            try:
                rolemention = discord.utils.get(ctx.guild.roles, name=role)
            except discord.NotFound:
                return await ctx.send(
                    "We can't find the role. Be sure to follow the syntax as in the exemple : **--level set 3 role_name**")
        if isinstance(role, int):
            try:
                rolemention = discord.utils.get(ctx.guild.roles, id=role)
            except discord.NotFound:
                return await ctx.send(
                    "We can't find the role. Be sure to follow the syntax as in the exemple : **--level set 3 role_name**")

        row = RoleDB.get_one_from_level(level, guild)
        if row:
            RoleDB.unset_level(row['level'], guild)
        RoleDB.set_level(role.id, guild, level)

        await ctx.send("Level setup", delete_after=2)

    # TODO: Faire une commande pour supprimer un role/level et pour voir les roles/levels déjà config

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

        bucket = self._cd.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            return

        userY = UserDB.get_one(user.id)
        guildY = GuildDB.get_one(message.guild.id)
        rankings = RankingsDB.get_user(userY, guildY)

        if not rankings:
            RankingsDB.create_ranking(userY, guildY)
            rankings = RankingsDB.get_user(userY, guildY)

        gain = randint(2, 10)

        rankings['xp'] += gain
        rankings['total'] += gain

        if rankings['xp'] >= rankings['reach']:
            if rankings["level"] >= 15:
                rankings['reach'] = round(rankings['reach'] * 1.05)
            elif 15 > rankings["level"] >= 12:
                rankings['reach'] = round(rankings['reach'] * 1.08)
            elif 12 > rankings["level"] >= 6:
                rankings['reach'] = round(rankings['reach'] * 1.2)
            else:
                rankings['reach'] = round(rankings['reach'] * 1.5)
            rankings['xp'] = 0
            rankings['level'] += 1

            try:
                await message.channel.send("{} is now level {}.".format(user.name, rankings['level']), delete_after=2)
            except discord.HTTPException:
                pass
            RankingsDB.update_user(userY, guildY, rankings)
            row = RoleDB.get_one_from_level(rankings['level'], guildY)
            if row:
                try:
                    role = discord.utils.get(
                        message.guild.roles, id=int(row["role_id"]))
                    await user.add_roles(role)
                except discord.HTTPException:
                    pass

        RankingsDB.update_user(userY, guildY, rankings)

    @commands.command()
    @checks.is_owner()
    async def fix_rank(self, ctx):
        levels_r = {}
        levels_t = {}
        reach = 20
        total = 0
        for x in range(25):
            if 0 < x < 6:
                reach = round(reach * 1.5)
                total += reach
                levels_r[x] = reach
                levels_t[x] = total

            if 6 <= x < 12:
                reach = round(reach * 1.2)
                total += reach
                levels_r[x] = reach
                levels_t[x] = total

            if 12 <= x < 15:
                reach = round(reach * 1.08)
                total += reach
                levels_r[x] = reach
                levels_t[x] = total

            if 15 <= x:
                reach = round(reach * 1.05)
                total += reach
                levels_r[x] = reach
                levels_t[x] = total

        rankings = RankingsDB.get_all()
        total_list = list(levels_t.values())
        print(total_list)
        for toto in rankings:
            if toto["total"] == 0:
                continue
            closest = min(filter(lambda x: x > toto["total"], total_list))
            for l, t in levels_t.items():
                if t == closest:
                    level = l
                    break
            reach = levels_r[level]
            xp = toto["total"] - levels_r[level-1]
            RankingsDB.update_user_id(toto["user_id"], toto["guild_id"], level, reach, xp )


# TODO: Ajouter des commandes pour voir les roles


def setup(bot):
    bot.add_cog(Level(bot))
