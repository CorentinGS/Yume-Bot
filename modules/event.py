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
import random
from math import floor

import discord
from discord.ext import commands

from modules.sql.guilddb import GuildDB
from modules.sql.messages_db import Message, MessageDB
from modules.sql.rankingsdb import RankingsDB
from modules.sql.roledb import RoleDB
from modules.sql.userdb import UserDB
from modules.utils import lists
from random import randint


class Event(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config
        self._cd = commands.CooldownMapping.from_cooldown(
            1.0, 2.0, commands.BucketType.user)

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if before.name != after.name:
            name = "{}#{}".format(after.name.lower(), after.discriminator)
            UserDB.update_name(after.id, name)

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        if before.name != after.name:
            name = "{}".format(after.name.lower())
            GuildDB.update_name(after.id, name)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """

        :param member: The member who joined the guild
        """

        guild = GuildDB.get_one(member.guild.id)

        if guild.greet:
            channel = self.bot.get_channel(int(guild.greet_chan))
            greet = random.choice(lists.greet)

            em = discord.Embed(timestamp=member.joined_at)
            em.set_author(name="Welcome", icon_url=member.avatar_url)
            em.set_footer(text=f'{member.name}')
            em.description = f"{greet}"
            await channel.send(embed=em)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """

        :param member: The member who has left
        """

        guild = GuildDB.get_one(member.guild.id)

        if guild.greet:
            try:
                channel = member.guild.get_channel(int(guild.greet_chan))
            except discord.HTTPException:
                pass
            else:
                greet = random.choice(lists.leave)

                em = discord.Embed(timestamp=member.joined_at)
                em.set_author(name="Bye", icon_url=member.avatar_url)
                em.set_footer(text=f'{member.name}')
                em.description = f"{greet}"
                await channel.send(embed=em)

    async def check(self, message):
        bucket = self._cd.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        ignored_guilds = [264445053596991498]

        if message.author.bot or not message.guild or retry_after or message.id in ignored_guilds:
            return False

        return True

    async def on_private_message(self, message):
        try:
            guild: discord.Guild = self.bot.get_guild(488765635439099914)
        except discord.HTTPException:
            return
        chan: discord.TextChannel = guild.get_channel(743198460055912478)
        user: discord.User = message.channel.recipient
        webhooks = await chan.webhooks()
        webhook = webhooks[0]

        await webhook.send(content=message.clean_content, username=user.name, avatar_url=user.avatar_url, wait=True)

    @staticmethod
    async def on_vip_message(message):
        user = UserDB.get_one(message.author.id)
        if not user.user_name or "{}#{}".format(message.author.name.lower(),
                                                message.author.discriminator) != user.user_name.lower():
            UserDB.update_name(message.author.id,
                               "{}#{}".format(message.author.name.lower(), message.author.discriminator))
        dt = message.created_at
        time = str(dt.year) + ("0" + str(dt.month) if dt.month < 10 else str(dt.month)) + (
            "0" + str(dt.day) if dt.day < 10 else str(dt.day))
        m = Message(guild_id=message.guild.id, message_id=message.id, user_id=message.author.id,
                    channel_id=message.channel.id, time_id=int(time))

        MessageDB.insert_message(m)

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

    async def on_rankings_message(self, message):
        if RankingsDB.is_ignored_chan(message.channel.id):
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

    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.DMChannel) and (
                not message.clean_content.startswith("--") or not message.author.bot):
            return await self.on_private_message(message)

        if not await self.check(message):
            return

        if message.guild.id in [488765635439099914, 631811291568144384, 618414922556112916, 740622438282428416]:
            await self.on_vip_message(message)

        await self.on_rankings_message(message)


def setup(bot):
    bot.add_cog(Event(bot))
