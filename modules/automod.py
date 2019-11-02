from datetime import datetime, timedelta

import discord
from discord.ext import commands

import modules.utils.checks as check
from modules.sanction import Sanction
from modules.utils.db import Settings
from modules.utils.format import Embeds
from modules.utils.format import Mod
from modules.utils.guildy import GuildY


class Checks:

    @staticmethod
    async def member_check(member: discord.Member):
        guild = member.guild
        now = datetime.now()
        create = member.created_at

        strike = await Settings().get_sanction_settings_member(str(member.id), str(guild.id))

        sanctions = len(strike)
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

            id = await Sanction().create_strike(message.author, "Strike", message.guild, "Mentions Spam")

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

            id = await Sanction().create_strike(message.author, "Strike", message.guild, "Discord Invite Link")

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
                await Sanction().create_strike(message.author, "Strike", message.guild, "Spamming")

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
        guildy = GuildY(member.guild)
        await guildy.get()

        glob = await Settings().get_glob_settings()

        # Check if the user has already been muted to avoid any sanctions bypass
        if member.id in guildy.mute:
            # Mute him again
            role = discord.utils.get(member.guild.roles, name="Muted")
            if not role:
                role = await member.guild.create_role(name="Muted", permissions=discord.Permissions.none(),
                                                      reason="Mute Role")
                for chan in member.guild.text_channels:
                    await chan.set_permissions(role, send_messages=False)
            await member.add_roles(role)

        # Check if the user is in the blacklist
        if 'Blacklist' in glob:
            if member.id in glob['Blacklist'] and guildy.bl:
                # Ban the member
                await member.guild.ban(member, reason="Blacklist")
            try:
                await member.send("you're in the blacklist ! If you think it's an error, ask here --> "
                                  "yume.network@protonmail.com")
            except discord.Forbidden:
                return

        if guildy.logging:
            sanctions, time = await Checks().member_check(member)
            em = await Mod().check_embed(member, member.guild, sanctions, time)
            if guildy.log_channel:
                channel = self.bot.get_channel(int(guildy.log_channel))
                if isinstance(channel, discord.TextChannel):
                    try:
                        await channel.send(embed=em)
                    except discord.Forbidden:
                        return


def setup(bot):
    bot.add_cog(Automod(bot))
