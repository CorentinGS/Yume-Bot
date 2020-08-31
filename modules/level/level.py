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
from datetime import datetime
from math import floor
from random import randint

import discord
from discord.ext import commands

from model.guild import Guild
from modules.sql.guilddb import GuildDB
from modules.sql.rankingsdb import RankingsDB
from modules.sql.roledb import RoleDB
from model.user import User
from modules.sql.userdb import UserDB
from modules.utils import checks


class Level(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config
        self._cd = commands.CooldownMapping.from_cooldown(
            2.0, 6.0, commands.BucketType.user)

    @commands.command()
    @commands.guild_only()
    async def rank(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.message.author

        rankings = RankingsDB.get_user(user.id, ctx.guild.id)
        if not rankings:
            RankingsDB.create_ranking(user.id, ctx.guild.id)
            rankings = RankingsDB.get_user(user.id, ctx.guild.id)

        rank = RankingsDB.get_rank(user.id, ctx.guild.id)
        em = discord.Embed()
        em.set_author(name=user.name, icon_url=user.avatar_url)
        em.add_field(name="**Rank**", value=f"{rank}", inline=False)
        em.add_field(name="**Level**", value=rankings["level"])
        em.add_field(name="**Progress**",
                     value="{} / {}".format(rankings['xp'], rankings['reach']))
        await ctx.send(embed=em)

    @commands.command(aliases=["scoreboard"])
    @commands.guild_only()
    async def leaderboard(self, ctx):
        guild_y = GuildDB.get_one(ctx.message.guild.id)
        scoreboard = RankingsDB.get_scoreboard(guild_y)

        em = discord.Embed(
            description="ScoreBoard",
            color=discord.Colour.magenta()
        )

        x = 0
        for user in scoreboard:
            member: discord.Member = discord.utils.get(ctx.guild.members, id=int(user))
            if not isinstance(member, discord.Member):
                RankingsDB.reset_user(member.id, ctx.guild.id)

            else:
                member_ranking = RankingsDB.get_user(member.id, ctx.guild.id)
                x += 1
                total = member_ranking['total']
                em.add_field(name=f"**{x} - {member.name}**", value=f"Total xp : {total}",
                             inline=False)

        await ctx.send(embed=em)

    @commands.group()
    @commands.guild_only()
    @checks.is_admin()
    async def level(self, ctx):
        if ctx.invoked_subcommand is None:
            # await ctx.invoke(self.get)
            return

    @level.command()
    @checks.is_admin()
    async def set(self, ctx, level: int, role: typing.Union[discord.Role, int]):
        if isinstance(role, int):
            try:
                role = discord.utils.get(ctx.guild.roles, id=role)
            except discord.NotFound:
                return await ctx.send(
                    "We can't find the role. Be sure to follow the syntax "
                    "as in the exemple : **--level set 3 role_name**")

        roles = RoleDB.get_one_from_level(level, ctx.guild.id)
        if roles:
            RoleDB.unset_level(roles['level'], ctx.guild.id)
        RoleDB.set_level(role.id, ctx.guild.id, level)

        await ctx.send("Level setup", delete_after=2)

    @level.command()
    @checks.is_admin()
    async def unset(self, ctx, level: int):
        roles = RoleDB.get_one_from_level(level, ctx.guild.id)
        if roles:
            RoleDB.unset_level(roles['level'], ctx.guild.id)
            await ctx.send("Level role removed", delete_after=2)
        else:
            await ctx.send("This level isn't setup...", delete_after=2)

    @level.command()
    @checks.is_admin()
    async def show(self, ctx):
        roles = RoleDB.get_levels(ctx.guild.id)
        em = discord.Embed(
            color=discord.Colour.blurple()
        )
        msg = "__Levels Roles__\n\n"

        for role in roles:

            role_discord = discord.utils.get(ctx.guild.roles, id=int(role['role_id']))

            if not role_discord:
                continue
            str1 = "**" + str(role['level']) + " |** " + role_discord.mention + "\n"
            msg = " ".join((msg, str1))
        em.description = msg
        await ctx.send(embed=em)

    async def checks_message(self, message: discord.Message) -> bool:
        user = message.author
        ignored_guilds = [264445053596991498]

        bucket = self._cd.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        RankingsDB.is_ignored_chan(message.channel.id)

        if (user.bot is True) \
                or (message.guild is None) \
                or (message.guild.id in ignored_guilds) \
                or retry_after:

            return False
        else:
            return True

    @staticmethod
    async def set_gain(message: discord.Message, rankings: dict) -> int:
        if rankings['level'] < 3:
            gain = randint(2, 12)
        elif 3 <= rankings['level'] < 6:
            gain = randint(8, 16)
        elif 6 <= rankings['level'] < 10:
            gain = randint(10, 18)
        elif 10 <= rankings['level'] < 20:
            gain = randint(12, 20)
        else:
            gain = randint(14, 22)
        if message.author in message.guild.premium_subscribers:
            gain += gain * 2
        return gain

    @staticmethod
    async def level_up(message: discord.Message, rankings: dict, user_id: int, guild_id: int):
        rankings['level'] += 1
        if rankings["level"] > 40:
            rankings['reach'] = floor(rankings['reach'] * 1.02)
        if 40 >= rankings["level"] > 35:
            rankings['reach'] = floor(rankings['reach'] * 1.04)
        if 35 >= rankings["level"] > 30:
            rankings['reach'] = floor(rankings['reach'] * 1.05)
        if 30 >= rankings["level"] > 21:
            rankings['reach'] = floor(rankings['reach'] * 1.07)
        elif 21 >= rankings["level"] > 10:
            rankings['reach'] = floor(rankings['reach'] * 1.1)
        elif 10 >= rankings["level"] > 6:
            rankings['reach'] = floor(rankings['reach'] * 1.25)
        else:
            rankings['reach'] = floor(rankings['reach'] * 1.6)
        rankings['xp'] = 0
        try:
            await message.channel.send("{} is now level {}.".format(message.author.name, rankings['level']),
                                       delete_after=2)
        except discord.HTTPException:
            pass
        RankingsDB.update_user(user_id, guild_id, rankings)
        return rankings

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """
        :param message: The message that has been sent
        """
        check: bool = await self.checks_message(message)
        if not check:
            return

        rankings = RankingsDB.get_user(message.author.id, message.guild.id)

        if not rankings:
            RankingsDB.create_ranking(message.author.id, message.guild.id)
            rankings = RankingsDB.get_user(message.author.id, message.guild.id)

        gain: int = await self.set_gain(message, rankings)

        rankings['xp'] += gain
        rankings['total'] += gain

        if rankings['xp'] >= rankings['reach']:
            rankings = await self.level_up(message, rankings, message.author.id, message.guild.id)

            roles = RoleDB.get_one_from_level(rankings['level'], message.guild.id)

            if roles:
                try:
                    role = discord.utils.get(
                        message.guild.roles, id=int(roles["role_id"]))
                    await message.author.add_roles(role)
                except discord.HTTPException:
                    pass

        RankingsDB.update_user(message.author.id, message.guild.id, rankings)
        t9 = datetime.now()

    @level.command()
    @checks.is_admin()
    async def ignore(self, ctx, chan: discord.TextChannel):
        await ctx.message.delete()
        if RankingsDB.is_ignored_chan(chan.id):
            await ctx.send("This channel is already ignored !")
        RankingsDB.set_ignored_chan(ctx.guild.id, chan.id)
        await ctx.send("This channel has been ignored : {} !".format(chan.mention), delete_after=5)

    @level.command()
    @checks.is_admin()
    async def unignore(self, ctx, chan: discord.TextChannel):
        await ctx.message.delete()
        if not RankingsDB.is_ignored_chan(chan.id):
            return await ctx.send("This channel is not ignored !")
        RankingsDB.delete_ignored_chan(ctx.guild.id, chan.id)
        await ctx.send("This channel has been unignored : {} !".format(chan.mention), delete_after=5)

    @level.command()
    @checks.is_admin()
    async def channels(self, ctx):
        channels = RankingsDB.get_ignored_chan(ctx.guild.id)
        em = discord.Embed(
            color=discord.Colour.blurple()
        )
        msg = "__Ignored Channels__\n\n"

        for channel in channels:

            channel_discord = discord.utils.get(ctx.guild.channels, id=int(channel['chan_id']))

            if not channel_discord:
                continue
            str1 = "*-* " + channel_discord.mention + "\n"
            msg = " ".join((msg, str1))
        em.description = msg
        await ctx.send(embed=em)

    @commands.command()
    @checks.is_owner()
    async def fix_rank(self, ctx):
        levels_r = {}
        levels_t = {}
        reach = 20
        total = 20
        levels_r[0] = 20
        levels_t[0] = 20

        for x in range(150):
            if 0 < x <= 6:
                reach = floor(reach * 1.6)
                total += reach
                levels_r[x] = reach
                levels_t[x] = total

            elif 6 < x <= 10:
                reach = floor(reach * 1.25)
                total += reach
                levels_r[x] = reach
                levels_t[x] = total

            elif 10 < x <= 21:
                reach = floor(reach * 1.1)
                total += reach
                levels_r[x] = reach
                levels_t[x] = total

            elif 21 < x <= 30:
                reach = floor(reach * 1.07)
                total += reach
                levels_r[x] = reach
                levels_t[x] = total

            elif 30 < x <= 35:
                reach = floor(reach * 1.05)
                total += reach
                levels_r[x] = reach
                levels_t[x] = total

            elif 35 < x <= 40:
                reach = floor(reach * 1.04)
                total += reach
                levels_r[x] = reach
                levels_t[x] = total

            elif 40 < x:
                reach = floor(reach * 1.02)
                total += reach
                levels_r[x] = reach
                levels_t[x] = total

        rankings = RankingsDB.get_all()
        total_list = list(levels_t.values())
        for toto in rankings:
            if toto["level"] < 3:
                continue
            closest = min(total_list, key=lambda x: abs(x - toto["total"]))
            if toto["total"] > closest:
                index = total_list.index(closest)
                closest = total_list[index + 1]
            for l, t in levels_t.items():
                if t == closest:
                    level = l
                    break
            reach = levels_r[level]

            xp = toto["total"] - levels_t[level - 1]
            RankingsDB.update_user_id(toto["user_id"], toto["guild_id"], level, reach, xp)

        await ctx.send("Fixed...")


# TODO: Ajouter des commandes pour voir les roles


def setup(bot):
    bot.add_cog(Level(bot))
