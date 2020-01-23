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
import asyncio
import typing
from typing import Union

import discord

from modules.sql.guilddb import GuildDB
from modules.sql.mutedb import MuteDB
from modules.sql.sanctionsdb import SanctionMethod
from modules.sql.userdb import UserDB
from modules.utils import checks
from modules.utils.converter import *
from modules.utils.db import Settings
from modules.utils.format import Embeds


class Check(commands.Cog):

    @staticmethod
    async def check(ctx, user: discord.Member):
        if ctx.message.author.top_role > user.top_role or ctx.author is ctx.guild.owner:
            return True
        else:
            await ctx.send("You can't do that because you don't have enough permissions...")
            return False


class Moderation(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    async def log_send(self, ctx, guild_id, embed):
        guildY = GuildDB.get_one(guild_id)
        if guildY.logging:
            try:
                channel = self.bot.get_channel(int(guildY.log_chan))
            except discord.HTTPException:
                return
            try:
                await channel.send(embed=embed)
            except discord.Forbidden:
                return
        else:
            await ctx.send(embed=embed)

    @commands.command(aliases=["sanctions", "modlog", "modlogs"])
    @checks.is_mod()
    async def sanction(self, ctx, user: typing.Union[discord.Member, discord.User, int]):
        """
        Get a sanction report
        """
        if isinstance(user, int):
            sanction = await SanctionMethod().find_sanction_id(ctx, user)
            em = Embeds.format_sanction_embed(sanction)
            await ctx.send(embed=em)
        if isinstance(user, discord.Member) or isinstance(user, discord.User):
            sanctions = await SanctionMethod().find_sanction_member(ctx, user, ctx.guild)
            em = Embeds.user_list_sanction_embed(sanctions)
            await ctx.send(embed=em)
        else:
            return

    @commands.command()
    @commands.bot_has_permissions(manage_channels=True)
    @checks.is_admin()
    async def slowmode(self, ctx, *, value: int = None):
        """
        Slowmode this channel
        """
        if not value or value == 0:
            await ctx.channel.edit(slowmode_delay=0)
        else:
            await ctx.channel.edit(slowmode_delay=value)
        await ctx.send("Channel slowmode has been changed !")

    @commands.command()
    @checks.is_admin()
    async def reset(self, ctx, member: discord.Member):
        """
        Reset this user sanctions
        """
        await Settings().rm_strike_settings(str(ctx.guild.id), str(member.id))

    @commands.command()
    @checks.is_mod()
    async def strike(self, ctx, user: discord.Member, *, reason: ModReason = None):
        """
        Strike him
        """
        perm = await Check().check(ctx, user)
        if perm is False:
            return

        id = await SanctionMethod().create_sanction(user, 'Strike', ctx.message.author, ctx.message.guild, reason)
        em = await Embeds().format_mod_embed(ctx, user, ctx.message.author, reason, 'strike', id)
        await self.log_send(ctx, ctx.message.guild.id, em)

    @commands.command(aliases=["chut", "tg"])
    @commands.bot_has_permissions(manage_channels=True, manage_roles=True)
    @checks.is_mod()
    async def mute(self, ctx, user: discord.Member, duration: str, *, reason: ModReason = None):

        """
        :param ctx: Command context
        :param user: The member to mute
        :param duration: The duration of the mute
        :param reason: the reason of the mute
        """

        perm = await Check().check(ctx, user)
        if perm is False:
            return

        guild = ctx.message.guild
        guildY = GuildDB.get_one(guild.id)
        userY = UserDB.get_one(user.id)

        unit = duration[-1]
        if unit == 's':
            time = int(duration[:-1])
        elif unit == 'm':
            time = int(duration[:-1]) * 60
        elif unit == 'h':
            time = int(duration[:-1]) * 3600
        elif unit == 'd':
            time = int(duration[:-1]) * 86400
        else:
            return await ctx.send('Invalid Unit! Use `s`, `m`, `h` or `d`.')

        if MuteDB.is_muted(userY, guildY):
            return await ctx.send('This user is already muted, you should '
                                  'unmute him first.')

        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            role = await ctx.guild.create_role(name="Muted", permissions=discord.Permissions.none(), reason="Mute Role")
            for chan in ctx.guild.text_channels:
                await chan.set_permissions(role, send_messages=False)
        await user.add_roles(role)

        MuteDB.set_mute(userY, guildY)

        id = await SanctionMethod().create_sanction(user, 'Mute', ctx.message.author, guild, reason, time)
        em = await Embeds().format_mod_embed(ctx, user, ctx.message.author, reason, 'mute', id, duration)

        await self.log_send(ctx, ctx.message.guild.id, em)

        await asyncio.sleep(time)

        if MuteDB.is_muted(userY, guildY):
            await ctx.invoke(self.unmute, user, True)

    @commands.command()
    @commands.bot_has_permissions(manage_channels=True, manage_roles=True)
    @checks.is_mod()
    async def unmute(self, ctx, user: discord.Member, auto: bool = False):

        if not auto:
            mod = ctx.message.author
        else:
            mod = "auto"

        role = discord.utils.get(ctx.guild.roles, name="Muted")
        guild = ctx.message.guild
        guildY = GuildDB.get_one(guild.id)
        userY = UserDB.get_one(user.id)

        if not MuteDB.is_muted(userY, guildY) or not role:
            return

        MuteDB.unset_mute(userY, guildY)

        try:
            await user.remove_roles(role)
        except discord.HTTPException:
            return

        em = await Embeds().format_mod_embed(ctx, user, mod, None, 'unmute')
        await self.log_send(ctx, ctx.message.guild.id, em)

    @commands.command(aliases=['out'])
    @commands.bot_has_permissions(kick_members=True)
    @checks.is_mod()
    async def kick(self, ctx, user: discord.Member, *, reason: ModReason = None):
        perm = await Check().check(ctx, user)
        if perm is False:
            return

        await ctx.guild.kick(user)

        id = await SanctionMethod().create_sanction(user, 'Kick', ctx.message.author, ctx.message.guild, reason)
        em = await Embeds().format_mod_embed(ctx, user, ctx.message.author, reason, 'kick', id)
        await self.log_send(ctx, ctx.message.guild.id, em)

    @commands.command(aliases=['preventban', 'preban', 'idban'])
    @checks.is_admin()
    async def hackban(self, ctx, id: MemberID, *, reason: ModReason = None):

        user = discord.Object(id=id)
        await ctx.guild.ban(user)

        banned = await self.bot.fetch_user(id)

        _id = await SanctionMethod().create_sanction(banned, 'Hackban', ctx.message.author, ctx.message.guild, reason)
        em = await Embeds().format_mod_embed(ctx, banned, ctx.message.author, reason, 'hackban', _id)

        await self.log_send(ctx, ctx.message.guild.id, em)

    @commands.command()
    @checks.is_admin()
    async def unban(self, ctx, id: MemberID):

        user = discord.Object(id=id)

        try:
            banned = await self.bot.fetch_user(id)
        except discord.NotFound:
            return await ctx.send("ID not found...")

        await ctx.guild.unban(user)

        em = await Embeds().format_mod_embed(ctx, banned, ctx.message.author, None, 'unban')

        await self.log_send(ctx, ctx.message.guild.id, em)

    @commands.command(aliases=['ciao'])
    @checks.is_mod()
    async def ban(self, ctx, user: discord.Member, *, reason: ModReason = None):
        perm = await Check().check(ctx, user)
        if perm is False:
            return

        await ctx.guild.ban(user, reason=reason, delete_message_days=7)

        id = await SanctionMethod().create_sanction(user, 'Ban', ctx.message.author, ctx.message.guild, reason)
        em = await Embeds().format_mod_embed(ctx, user, ctx.message.author, reason, 'ban', id)

        await self.log_send(ctx, ctx.message.guild.id, em)

    @commands.command(case_insensitive=True, aliases=['clean', 'clear'])
    @checks.is_mod()
    async def purge(self, ctx, amount: int, arg: str = None):
        if not arg:
            await ctx.channel.purge(limit=amount, bulk=True)
        elif arg.lower() == 'text':
            def is_text(m):
                return not m.attachments

            await ctx.channel.purge(limit=amount + 1, check=is_text, bulk=True)
        elif arg.lower() == "image":
            def is_image(m):
                return m.attachments

            await ctx.channel.purge(limit=amount + 1, check=is_image, bulk=True)

    @commands.command(aliases=['deafen'])
    @checks.is_mod()
    async def deaf(self, ctx, user: discord.Member):
        await user.edit(deafen=True)

    @commands.command(aliases=['undeafen'])
    @checks.is_mod()
    async def undeaf(self, ctx, user: discord.Member):
        await user.edit(deafen=False)

    @commands.command(aliases=['novoice'])
    @checks.is_mod()
    async def vmute(self, ctx, user: discord.Member):
        await user.edit(mute=True)

    @commands.command()
    @checks.is_mod()
    async def unvmute(self, ctx, user: discord.Member):
        await user.edit(mute=False)

    @commands.command()
    @checks.is_mod()
    async def nick(self, ctx, user: discord.Member, name: str = None):
        await user.edit(nick=name)

    @commands.command()
    @checks.is_admin()
    async def massban(self, ctx, *members: MemberID):
        try:
            for member_id in members:
                await ctx.guild.ban(discord.Object(id=member_id), reason="{} - massban".format(ctx.message.author))
        except Exception as e:
            return await ctx.send(e)

        guild = ctx.message.guild
        guildY = GuildDB.get_one(guild.id)

        if guildY.logging:
            channel = self.bot.get_channel(int(guildY.log_chan))
            await channel.send(f'{len(members)} users were banned')
        else:
            await ctx.send(f'{len(members)} users were banned')

    @commands.command()
    @checks.is_admin()
    async def mention(self, ctx, role: str):
        rolemention = discord.utils.get(ctx.guild.roles, name=role)

        if not rolemention.mentionable:
            await rolemention.edit(mentionable=True)

        await ctx.send(rolemention.mention)
        await rolemention.edit(mentionable=False)

    @commands.command()
    @checks.is_admin()
    async def annonce(self, ctx, role: str, *, content):
        rolemention = discord.utils.get(ctx.guild.roles, name=role)

        if not rolemention.mentionable:
            await rolemention.edit(mentionable=True)

        await ctx.send("{} \n{}".format(rolemention.mention, content))
        await rolemention.edit(mentionable=False)

    # source:   https://github.com/nmbook/FalcomBot-cogs/blob/master/topic/topic.py

    @commands.group()
    @commands.guild_only()
    async def topic(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.get)

    @topic.command()
    async def get(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel

        if channel.guild != ctx.guild:
            return

        if not channel.topic:
            return await ctx.send(f'No topic is set for {channel.mention}')

        title = "#{}".format(str(channel))
        url = "https://discordapp.com/channels/{}/{}/" \
            .format(channel.guild.id, channel.id)
        description = channel.topic.replace("](", "]\\(")
        embed = discord.Embed(
            title=title,
            url=url,
            description=description)
        embed.set_footer(text=channel.guild)

        await ctx.send(embed=embed)

    @topic.command()
    @checks.is_admin()
    async def set(self, ctx, channel: discord.TextChannel = None, *, topic: str):
        if channel is None:
            channel = ctx.channel

        if channel.guild != ctx.guild:
            return

        reason = f"Topic edit by request of {ctx.author} ({ctx.author.id})"
        try:
            await channel.edit(topic=topic, reason=reason)
        except (discord.Forbidden, discord.HTTPException):
            return await ctx.send("I don't have permission to edit this topic!")

    @commands.command()
    @checks.is_admin()
    @checks.is_vip()
    async def addrole(self, ctx, role: Union[str, discord.Role]):
        """
        Add a role to everyone
        """
        if not isinstance(role, discord.Role):
            try:
                role = discord.utils.get(ctx.guild.roles, name=role)
            except discord.NotFound:
                return await ctx.send("I can't find that role")
        count = 0
        for user in ctx.guild.members:
            await user.add_roles(role)
            await asyncio.sleep(1)
            count += 1
            if count == 20:
                await asyncio.sleep(3)
                count = 0


# TODO: Separer les commandes mod et admin

def setup(bot):
    bot.add_cog(Moderation(bot))
