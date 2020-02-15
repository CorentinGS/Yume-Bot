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

from datetime import datetime

import discord
from discord.ext import commands

import modules.utils.checks as check
from modules.sql.blacklistdb import BlacklistDB
from modules.sql.guilddb import GuildDB
from modules.sql.sanctionsdb import SanctionsDB
from modules.sql.userdb import UserDB
from modules.utils.format import Mod


class Checks:

    @staticmethod
    async def member_check(member: discord.Member):
        guild = GuildDB.get_one(member.guild.id)
        now = datetime.now()
        create = member.created_at

        strikes = SanctionsDB.get_sanctions_from_guild_user(member.guild, member)

        sanctions = len(strikes)
        time = (now - create).days

        return sanctions, time


class Automod(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config
        self.mention_limit = 6

    @staticmethod
    async def immune(message):
        return await check.is_immune(message)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """

        :param member: The member who joined the guild
        """
        guild = GuildDB.get_one(member.guild.id)
        user = UserDB.get_one(member.id)

        # Check if the user has already been muted to avoid any sanctions bypass
        if UserDB.is_muted(guild, user):
            # Mute him again
            role = discord.utils.get(member.guild.roles, name="Muted")
            if not role:
                role = await member.guild.create_role(name="Muted", permissions=discord.Permissions.none(),
                                                      reason="Mute Role")
                for chan in member.guild.text_channels:
                    await chan.set_permissions(role, send_messages=False)
            await member.add_roles(role)

        # Check if the user is in the blacklist
        if BlacklistDB.is_blacklist(user):
            if GuildDB.has_blacklist(guild):
                # Ban the member
                await member.guild.ban(member, reason="Blacklist")
            try:
                await member.send("you're in the blacklist ! If you think it's an error, ask here --> "
                                  "yume.network@protonmail.com")
            except discord.Forbidden:
                return

        if GuildDB.has_logging(guild):
            sanctions, time = await Checks().member_check(member)
            em = await Mod().check_embed(member, member.guild, sanctions, time)
            if guild.log_chan:
                channel = self.bot.get_channel(int(guild.log_chan))
                if isinstance(channel, discord.TextChannel):
                    try:
                        await channel.send(embed=em)
                    except discord.Forbidden:
                        return


def setup(bot):
    bot.add_cog(Automod(bot))
