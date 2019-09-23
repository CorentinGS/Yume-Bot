from datetime import datetime, timedelta

import discord
from discord.ext import commands

from modules.sanction import Sanction
from modules.utils.db import Settings
from modules.utils.format import Embeds
from modules.utils.format import Mod


class Checks:

    @staticmethod
    async def member_check(member: discord.Member):
        guild = member.guild
        now = datetime.now()
        create = member.created_at

        strike = await Settings().get_sanction_settings_user(str(member.id), str(guild.id))

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
        guild = message.guild
        author = message.author
        mentions = set(message.mentions)

        settings = await Settings().get_server_settings(str(guild.id))

        if len(mentions) >= self.mention_limit:
            try:
                await message.delete()
            except discord.HTTPException:
                return False

            id = await Sanction().create_strike(message.author, "Strike", message.guild, "Mentions Spam")

            em = await Embeds().format_automod_embed(author, "Mention spam", id, message)
            if settings['logging'] is True:
                if 'LogChannel' in settings:
                    channel = self.bot.get_channel(int(settings['LogChannel']))
                    try:
                        await channel.send(embed=em)
                    except discord.Forbidden:
                        await message.channel.send(embed=em)
            else:
                await message.channel.send(embed=em)

            return True
        else:
            return False

    async def check_invite(self, message):
        guild = message.guild
        author = message.author

        settings = await Settings().get_server_settings(str(guild.id))

        if "discord.gg/" in message.content:
            try:
                await message.delete()
            except discord.HTTPException:
                return False

            id = await Sanction().create_strike(message.author, "Strike", message.guild, "Discord Invite Link")

            em = await Embeds().format_automod_embed(author, "Discord Invite Link", id, message)
            if settings['logging'] is True:
                if 'LogChannel' in settings:
                    channel = self.bot.get_channel(int(settings['LogChannel']))
                    try:
                        await channel.send(embed=em)
                    except discord.Forbidden:
                        await message.channel.send(embed=em)
            else:
                await message.channel.send(embed=em)

            return True
        else:
            return False

    async def raid_check(self, message):

        mode = "soft"
        m_max = 3

        guild = message.guild
        author = message.author

        settings = await Settings().get_server_settings(str(guild.id))

        if not message.author.joined_at > datetime.utcnow() + timedelta(minutes=-360):
            mode = "strict"

        m_count = 0
        async for m in message.channel.history(after=(datetime.utcnow() + timedelta(seconds=-10))):
            if m.author == author:
                m_count += 1
            if m_count > m_max:
                await message.delete()
                await message.channel.send(f"No spamming, {message.author.mention}", delete_after=5)
                id = await Sanction().create_strike(message.author, "Strike", message.guild, "Spamming")

                # TODO: Si mode strict, mute l'user...

                return True
            else:
                return False

    '''
    async def auto_sanction(self, message):

        sanctions = await Settings().get_sanction_settings_user(str(author.id), str(guild.id))
        count = len(sanctions)

        # TODO: Automatiser les sanctions selon les comportements
    '''

    @commands.Cog.listener()
    async def on_message(self, message):
        if (
                not message.guild
                or message.author.bot
        ):
            return

        set = await Settings().get_server_settings(str(message.guild.id))

        if "automod" not in set:
            return

        if set["automod"] is True:

            deleted = await self.check_mention_spam(message)
            if not deleted:
                await self.check_invite(message)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """

        :param member: The member who joined the guild
        """
        guild = member.guild
        set = await Settings().get_server_settings(str(guild.id))
        glob = await Settings().get_glob_settings()

        # Check if the user has already been muted to avoid any sanctions bypass
        if 'Mute' in set and member.id in set['Mute']:
            # Mute him again
            for chan in guild.text_channels:
                await chan.set_permissions(member, send_messages=False)
                await Sanction().create_strike(member.author, "Strike", member.guild, "Try to mute Bypass")

        '''
        # Check if the user is in the blacklist
        if 'Blacklist' in glob:
            if member.id in glob['Blacklist'] and set["bl"] is True:
                # Ban the member
                await guild.ban(member, reason="Blacklist")
            try:
                await member.send("you're in the blacklist ! If you think it's an error, ask here --> "
                              "yume.network@protonmail.com")
            except discord.Forbidden:
                return
        '''

        if set['logging'] is True:
            sanctions, time = await Checks().member_check(member)
            em = await Mod().check_embed(member, guild, sanctions, time)
            if 'LogChannel' in set:
                try:
                    channel = self.bot.get_channel(int(set['LogChannel']))
                except discord.HTTPException:
                    return
                try:
                    await channel.send(embed=em)
                except discord.Forbidden:
                    return


def setup(bot):
    bot.add_cog(Automod(bot))
