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
from collections import defaultdict
from datetime import datetime, timedelta, timezone

import discord
from discord.ext import commands

import modules.utils.checks as check
from modules.sql.guilddb import GuildDB
from modules.sql.mutedb import MuteDB
from modules.sql.sanctionsdb import SanctionsDB
from modules.sql.userdb import UserDB
from modules.utils.format import Mod


class Checks:

    @staticmethod
    async def member_check(member: discord.Member):
        guild = GuildDB.get_one(member.guild.id)
        now = datetime.now()
        create = member.created_at

        strikes = SanctionsDB.get_sanctions_from_guild_user(member.guild.id, member.id)

        sanctions = len(strikes)
        time = (now - create).days

        return sanctions, time


class CooldownByContent(commands.CooldownMapping):
    def _bucket_key(self, message):
        return message.channel.id, message.content


class SpamChecker:

    def __init__(self):
        self.by_content = CooldownByContent.from_cooldown(15, 17.0, commands.BucketType.member)
        self.by_user = commands.CooldownMapping.from_cooldown(10, 12.0, commands.BucketType.user)
        self.last_join = None
        self.new_user = commands.CooldownMapping.from_cooldown(30, 35.0, commands.BucketType.channel)

    def is_new(self, member):
        now = datetime.utcnow()
        seven_days_ago = now - timedelta(days=7)
        two_month_ago = now - timedelta(days=60)
        return member.created_at > two_month_ago and member.joined_at > seven_days_ago

    def is_spamming(self, message):
        if message.guild is None:
            return False

        current = message.created_at.replace(tzinfo=timezone.utc).timestamp()

        if self.is_new(message.author):
            new_bucket = self.new_user.get_bucket(message)
            if new_bucket.update_rate_limit(current):
                return True

        user_bucket = self.by_user.get_bucket(message)
        if user_bucket.update_rate_limit(current):
            return True

        content_bucket = self.by_content.get_bucket(message)
        if content_bucket.update_rate_limit(current):
            return True

        return False

    def is_fast_join(self, member):
        joined = member.joined_at or datetime.utcnow()
        if self.last_join is None:
            self.last_join = joined
            return False
        is_fast = (joined - self.last_join).total_seconds() <= 4.0
        self.last_join = joined
        return is_fast


class Automod(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config
        self.mention_limit = 6
        self._spam_check = defaultdict(SpamChecker)

    async def check_raid(self, guild_id, member, message):

        checker = self._spam_check[guild_id]
        if not checker.is_spamming(message):
            return

        try:
            await member.ban(reason='Auto-ban from spam (strict raid mode ban)')
        except discord.HTTPException:
            return

    @staticmethod
    async def immune(message):
        return await check.is_immune(message)

    '''
    @commands.Cog.listener()
    async def on_message(self, message):
        author = message.author
        if author.id in (self.bot.user.id, self.bot.owner_id):
            return

        if message.guild is None:
            return

        if author.bot or not isinstance(author, discord.Member):
            return

        # check for raid mode stuff
        # await self.check_raid(message.guild.id, author, message)

        # auto-ban tracking for mention spams begin here
        if len(message.mentions) <= 3:
            return

        if not self.mention_limit:
            return

        # check if it meets the thresholds required
        mention_count = sum(not m.bot and m.id != author.id for m in message.mentions)
        if mention_count < self.mention_limit:
            return

        # if message.channel.id in config.safe_mention_channel_ids:
        # return

        try:
            await author.ban(reason=f'Spamming mentions ({mention_count} mentions)')
        except Exception as e:
            # log.info(f'Failed to autoban member {author} (ID: {author.id}) in guild ID {guild_id}')
            return
        else:
            await message.channel.send(f'Banned {author} (ID: {author.id}) for spamming {mention_count} mentions.')
    '''

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """

        :param member: The member who joined the guild
        """
        guild = GuildDB.get_one(member.guild.id)
        user = UserDB.get_one(member.id)

        # Check if the user has already been muted to avoid any sanctions bypass
        if MuteDB.is_muted(member.id, member.guild.id):
            # Mute him again
            role = discord.utils.get(member.guild.roles, name="Muted")
            if not role:
                role = await member.guild.create_role(name="Muted", permissions=discord.Permissions.none(),
                                                      reason="Mute Role")
                for chan in member.guild.text_channels:
                    await chan.set_permissions(role, send_messages=False)
            await member.add_roles(role)
        if guild.logging:
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
