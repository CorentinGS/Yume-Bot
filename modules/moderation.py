import asyncio
import typing
from typing import Union

import discord

from modules.sanction import Sanction
from modules.utils import checks
from modules.utils.converter import *
from modules.utils.db import Settings
from modules.utils.format import Embeds


class Check(commands.Cog):

    @staticmethod
    async def check(ctx, user: discord.Member):
        if ctx.message.author.top_role > user.top_role:
            return True
        else:
            await ctx.send("You can't do that because you don't have enough permissions...")
            return False


class Moderation(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.command()
    @commands.guild_only()
    async def sanction(self, ctx, sanction: typing.Union[discord.Member, discord.User, int]):
        await ctx.message.delete()
        if sanction is int:
            em = await Sanction().find_sanction_id(ctx, sanction)
            await ctx.send(embed=em)
        if sanction is discord.Member or discord.User:
            em = await Sanction().find_sanction_member(ctx, sanction, ctx.guild)
            await ctx.send(embed=em)
        else:
            return

    @commands.command()
    @checks.is_admin()
    async def reset(self, ctx, member: discord.Member):
        await Settings().rm_strike_settings(str(ctx.guild.id), str(member.id))

    @commands.command()
    @checks.is_mod()
    async def strike(self, ctx, user: discord.Member, *, reason: ModReason = None):
        perm = await Check().check(ctx, user)
        if perm is False:
            return
        await ctx.message.delete()
        set = await Settings().get_server_settings(str(ctx.guild.id))
        id = await Sanction().create_sanction(user, 'Strike', ctx.message.author, ctx.message.guild, reason)
        em = await Embeds().format_mod_embed(ctx, user, ctx.message.author, reason, 'strike', id)
        if set['logging'] is True:
            if 'LogChannel' in set:
                channel = self.bot.get_channel(int(set['LogChannel']))
                try:
                    await channel.send(embed=em)
                except discord.Forbidden:
                    await ctx.send(embed=em)
        else:
            await ctx.send(embed=em)

    @commands.command(aliases=["chut", "tg"])
    @checks.is_mod()
    async def mute(self, ctx, user: discord.Member, duration: str, *, reason: ModReason = None):

        """
        :param user: The member to mute
        :param duration: The duration of the mute
        :param reason: the reason of the mute
        """

        perm = await Check().check(ctx, user)
        if perm is False:
            return
        guild = ctx.message.guild
        set = await Settings().get_server_settings(str(guild.id))

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

        if not 'Mute' in set:
            set['Mute'] = []

        if user.id in set['Mute']:
            return await ctx.send('This user is already muted, '
                                  'use {}unmute to umute him.'.format(self.bot.config['prefix']))

        set['Mute'].append(user.id)
        await Settings().set_server_settings(str(guild.id), set)

        for chan in ctx.guild.text_channels:
            await chan.set_permissions(user, send_messages=False)

        id = await Sanction().create_sanction(user, 'Mute', ctx.message.author, guild, reason, time)
        em = await Embeds().format_mod_embed(ctx, user, ctx.message.author, reason, 'mute', id, duration)

        if set['logging'] is True:
            if 'LogChannel' in set:
                channel = self.bot.get_channel(int(set['LogChannel']))
                try:
                    await channel.send(embed=em)
                except discord.Forbidden:
                    await ctx.send(embed=em)

        else:
            await ctx.send(embed=em)

        await asyncio.sleep(time)

        set = await Settings().get_server_settings(str(guild.id))

        if user.id in set['Mute']:
            await ctx.invoke(self.unmute, user, True)
        else:
            return

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(f'Missing an argument.\n`{error}`')

    @commands.command()
    @checks.is_mod()
    async def unmute(self, ctx, user: discord.Member, auto: bool = False):
        guild = ctx.message.guild
        set = await Settings().get_server_settings(str(guild.id))

        if not auto:
            mod = ctx.message.author
        else:
            mod = "auto"

        for chan in ctx.guild.text_channels:
            await chan.set_permissions(user, overwrite=None)

        if set['Mute']:
            if user.id not in set['Mute']:
                return
            set['Mute'].remove(user.id)
        await Settings().set_server_settings(str(guild.id), set)

        em = await Embeds().format_mod_embed(ctx, user, mod, None, 'unmute')
        if set['logging'] is True:
            if 'LogChannel' in set:
                channel = self.bot.get_channel(int(set['LogChannel']))
                try:
                    await channel.send(embed=em)
                except discord.Forbidden:
                    await ctx.send(embed=em)
        else:
            await ctx.send(embed=em)

    @commands.command(aliases=['out'])
    @checks.is_mod()
    async def kick(self, ctx, user: discord.Member, *, reason: ModReason = None):
        perm = await Check().check(ctx, user)
        if perm is False:
            return
        server = str(ctx.guild.id)
        setting = await Settings().get_server_settings(server)

        await ctx.message.delete()

        await ctx.guild.kick(user)
        id = await Sanction().create_sanction(user, 'Kick', ctx.message.author, ctx.message.guild, reason)
        em = await Embeds().format_mod_embed(ctx, user, ctx.message.author, reason, 'kick', id)

        if setting['logging'] is True:
            if 'LogChannel' in setting:
                channel = self.bot.get_channel(int(setting['LogChannel']))
                try:
                    await channel.send(embed=em)
                except discord.Forbidden:
                    await ctx.send(embed=em)
        else:
            await ctx.send(embed=em)

    @commands.command(aliases=['preventban', 'preban', 'idban'])
    @checks.is_admin()
    async def hackban(self, ctx, id: MemberID, *, reason: ModReason = None):

        await ctx.message.delete()
        user = discord.Object(id=id)
        await ctx.guild.ban(user)

        banned = await self.bot.fetch_user(id)

        _id = await Sanction().create_sanction(banned, 'Hackban', ctx.message.author, ctx.message.guild, reason)
        em = await Embeds().format_mod_embed(ctx, banned, ctx.message.author, reason, 'hackban', _id)

        server = str(ctx.guild.id)
        setting = await Settings().get_server_settings(server)

        if setting['logging'] is True:
            if 'LogChannel' in setting:
                channel = self.bot.get_channel(int(setting['LogChannel']))
                try:
                    await channel.send(embed=em)
                except discord.Forbidden:
                    await ctx.send(embed=em)
        else:
            await ctx.send(embed=em)

    @commands.command()
    @checks.is_admin()
    async def unban(self, ctx, id: MemberID):

        await ctx.message.delete()
        user = discord.Object(id=id)
        banned = await self.bot.fetch_user(id)

        await ctx.guild.unban(user)

        em = await Embeds().format_mod_embed(ctx, banned, ctx.message.author, None, 'unban')
        server = str(ctx.guild.id)
        setting = await Settings().get_server_settings(server)

        if setting['logging'] is True:
            if 'LogChannel' in setting:
                channel = self.bot.get_channel(int(setting['LogChannel']))
                try:
                    await channel.send(embed=em)
                except discord.Forbidden:
                    await ctx.send(embed=em)
        else:
            await ctx.send(embed=em)

    @commands.command(aliases=['ciao'])
    @checks.is_mod()
    async def ban(self, ctx, user: discord.Member, *, reason: ModReason = None):
        perm = await Check().check(ctx, user)
        if perm is False:
            return
        await ctx.message.delete()

        await ctx.guild.ban(user, reason=reason, delete_message_days=7)

        id = await Sanction().create_sanction(user, 'Ban', ctx.message.author, ctx.message.guild, reason)
        em = await Embeds().format_mod_embed(ctx, user, ctx.message.author, reason, 'ban', id)

        server = str(ctx.guild.id)
        setting = await Settings().get_server_settings(server)

        if setting['logging'] is True:
            if 'LogChannel' in setting:
                channel = self.bot.get_channel(int(setting['LogChannel']))
                try:
                    await channel.send(embed=em)
                except discord.Forbidden:
                    await ctx.send(embed=em)

        else:
            await ctx.send(embed=em)

    @commands.command(aliases=['clean', 'clear'])
    @checks.is_mod()
    async def purge(self, ctx, amount: int):

        await ctx.message.delete()

        if amount > 100:
            return await ctx.send("You can't purge more than 100messages.")
        try:
            await ctx.channel.purge(limit=amount + 1)

        except discord.HTTPException:
            pass

    @commands.command(aliases=['deafen'])
    @checks.is_mod()
    async def deaf(self, ctx, user: discord.Member):
        await ctx.message.delete()

        await user.edit(deafen=True)

    @commands.command(aliases=['undeafen'])
    @checks.is_mod()
    async def undeaf(self, ctx, user: discord.Member):
        await ctx.message.delete()

        await user.edit(deafen=False)

    @commands.command(aliases=['novoice'])
    @checks.is_mod()
    async def vmute(self, ctx, user: discord.Member):
        await ctx.message.delete()

        await user.edit(mute=True)

    @commands.command()
    @checks.is_mod()
    async def unvmute(self, ctx, user: discord.Member):
        await ctx.message.delete()

        await user.edit(mute=False)

    @commands.command()
    @checks.is_mod()
    async def nick(self, ctx, user: discord.Member, name: str = None):
        await ctx.message.delete()

        await user.edit(nick=name)

    @commands.command()
    @checks.is_admin()
    async def massban(self, ctx, *members: MemberID):
        await ctx.message.delete()

        try:
            for member_id in members:
                await ctx.guild.ban(discord.Object(id=member_id), reason="{} - massban".format(ctx.message.author))

        except Exception as e:
            return await ctx.send(e)

        server = str(ctx.guild.id)
        setting = await Settings().get_server_settings(server)

        if setting['logging'] is True:
            if 'LogChannel' in setting:
                channel = self.bot.get_channel(int(setting['LogChannel']))
                await channel.send(f'{len(members)} users were banned')

        else:
            await ctx.send(f'{len(members)} users were banned')

    @commands.command()
    @checks.is_admin()
    async def mention(self, ctx, role: str):

        await ctx.message.delete()
        rolemention = discord.utils.get(ctx.guild.roles, name=role)

        if not rolemention.mentionable:
            await rolemention.edit(mentionable=True)

        await ctx.send(rolemention.mention)
        await rolemention.edit(mentionable=False)

    @commands.command()
    @checks.is_admin()
    async def annonce(self, ctx, role: str, *, content):
        await ctx.message.delete()
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
        await ctx.message.delete()

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
        await ctx.message.delete()

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
    async def addrole(self, ctx, role: Union[str, discord.Role]):
        await ctx.message.delete()

        if not role is discord.Role:
            try:
                role = discord.utils.get(ctx.guild.roles, name=role)
            except discord.NotFound:
                return await ctx.send("I can't find that role")

        for user in ctx.guild.members:
            await user.add_roles(role)
            await asyncio.sleep(1)


def setup(bot):
    bot.add_cog(Moderation(bot))
