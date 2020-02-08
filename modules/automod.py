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

from datetime import datetime, timedelta

import discord
from discord.ext import commands

import modules.utils.checks as check
from modules.sql.blacklistdb import BlacklistDB
from modules.sql.guilddb import GuildDB
from modules.sql.sanctionsdb import SanctionMethod, SanctionsDB
from modules.sql.userdb import UserDB
from modules.utils.format import Embeds
from modules.utils.format import Mod
from modules.utils.guildy import GuildY


class Checks:

    @staticmethod
    async def member_check(member: discord.Member):
        guild = GuildDB.get_one(member.guild.id)
        now = datetime.now()
        create = member.created_at

        strikes = SanctionsDB.get_sanctions_from_guild_user(guild, member)

        sanctions = len(strikes)
        time = (now - create).days

        return sanctions, time


class Automod(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config
        self.mention_limit = 6

    async def check_mention_spam(self, message):
        author = message.author
        mentions = set(message.mentions)

        guildy = GuildY(message.guild)
        await guildy.get()

        if await self.immune(message):
            return

        if len(mentions) >= self.mention_limit:
            try:
                await message.delete()
            except discord.HTTPException:
                return False

            id = await SanctionMethod().create_strike(message.author, "Strike", message.guild, "Mentions Spam")

            em = await Embeds().format_automod_embed(author, "Mention spam", id, message)
            if guildy.logging:
                channel = self.bot.get_channel(int(guildy.log_channel))
                try:
                    await channel.send(embed=em)
                except discord.Forbidden:
                    await message.channel.send(embed=em)
            else:
                await message.channel.send(embed=em)

            return True
        else:
            return False

    @staticmethod
    async def immune(message):
        return await check.is_immune(message)

    async def check_invite(self, message):
        author = message.author

        guildy = GuildY(message.guild)
        await guildy.get()

        if await self.immune(message):
            return

        if "discord.gg/" in message.content:
            try:
                await message.delete()
            except discord.HTTPException:
                return False

            id = await SanctionMethod().create_strike(message.author, "Strike", message.guild, "Discord Invite Link")

            em = await Embeds().format_automod_embed(author, "Discord Invite Link", id, message)
            if guildy.logging:

                channel = self.bot.get_channel(int(guildy.log_channel))
                try:
                    await channel.send(embed=em)
                except discord.Forbidden:
                    await message.channel.send(embed=em)
            else:
                await message.channel.send(embed=em)
            return True
        else:
            return False

    @staticmethod
    async def spam_check(message):

        m_max = 3
        author = message.author
        m_count = 0

        async for m in message.channel.history(after=(datetime.utcnow() + timedelta(seconds=-10))):
            if m.author == author:
                m_count += 1
            if m_count > m_max:
                await message.delete()
                await message.channel.send(f"No spamming, {message.author.mention}", delete_after=5)
                await SanctionMethod().create_strike(message.author, "Strike", message.guild, "Spamming")

                # TODO: Si mode strict, mute l'user...

                return True
            else:
                return False

    @commands.Cog.listener()
    async def on_message(self, message):
        if (
                not message.guild
                or message.author.bot
        ):
            return

        guildy = GuildY(message.guild)
        await guildy.get()

        if guildy.automod:
            deleted = await self.check_mention_spam(message)
            if not deleted:
                await self.check_invite(message)

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

    @commands.group()
    @check.is_admin()
    async def automod(self, ctx):
        return

    @automod.command()
    @check.is_admin()
    async def setup(self, ctx):
        await ctx.send("Not ready yet ! Be patient dear ;)")

    @automod.command()
    @check.is_admin()
    async def gate(self, ctx):
        await ctx.send("Not ready yet ! Be patient dear ;)")

    # TODO: Gateway


def setup(bot):
    bot.add_cog(Automod(bot))
