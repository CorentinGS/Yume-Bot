import asyncio
import datetime

import discord
from discord.ext import commands

from modules.utils.db import Settings
from modules.utils.format import Embeds


class Moderation:

    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.command(aliases=["chut", "tg"])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, user: discord.Member, duration):

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
            return await ctx.send('This user is already muted, use {}unmute to umute him.'.format(self.bot.config['prefix']))

        set['Mute'].append(user.id)
        await Settings().set_server_settings(str(guild.id), set)


        try:
            for chan in ctx.guild.text_channels:
                await chan.set_permissions(user, send_messages=False)
        except discord.HTTPException:
            success = False
            return await ctx.send('Failed to Mute {}'.format(user))
        else:
            success = True
 

        em = await Embeds().format_mod_embed(ctx, user, success, 'mute', duration)

        if set['logging'] is True:
            if 'LogChannel' in set:
                channel = self.bot.get_channel(int(set['LogChannel']))
                await channel.send(embed=em)
            else:
                pass
        else:
            await ctx.send(embed=em)

        await asyncio.sleep(time)

        if user.id in set['Mute']:
            await ctx.invoke(self.unmute, user)
        else:
            return

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, user: discord.Member):
        guild = ctx.message.guild
        set = await Settings().get_server_settings(str(guild.id))


        try:
            for chan in ctx.guild.text_channels:
                await chan.set_permissions(user, overwrite=None)
        except discord.HTTPException:
            success = False
            return await ctx.send('Failed to unmute {}'.format(user))
        else:
            success = True

        
        if set['Mute']:
            if user.id not in set['Mute']:
                return
            set['Mute'].remove(user.id)
        await Settings().set_server_settings(str(guild.id), set)

        em = await Embeds().format_mod_embed(ctx, user, success, 'unmute')
        if set['logging'] is True:
            if 'LogChannel' in set:
                channel = self.bot.get_channel(int(set['LogChannel']))
                await channel.send(embed=em)
            else:
                pass
        else:
            await ctx.send(embed=em)

    @commands.command(aliases=['out'])
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason: str = None):
        server = str(ctx.guild.id)
        setting = await Settings().get_server_settings(server)

        await ctx.message.delete()

        try:
            await ctx.guild.kick(user)

        except discord.Forbidden:
            success = False
            return await ctx.send('Forbidden')

        else:
            success = True

        em = await Embeds().format_mod_embed(ctx, user, success, 'kick')

        if setting['logging'] is True:
            if 'LogChannel' in setting:
                channel = self.bot.get_channel(int(setting['LogChannel']))
                await channel.send(embed=em)
            else:
                pass
        else:
            await ctx.send(embed=em)

    @commands.command(aliases=['preventban', 'preban', 'idban'])
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def hackban(self, ctx, id: int, *, reason: str = None):

        await ctx.message.delete()
        user = discord.Object(id=id)

        try:
            await ctx.guild.ban(user)

        except discord.Forbidden:
            success = False
            return await ctx.send("Forbidden")

        else:
            success = True

        banned = await self.bot.get_user_info(id)

        em = await Embeds().format_mod_embed(ctx, banned, success, 'hackban')

        server = str(ctx.guild.id)
        setting = await Settings().get_server_settings(server)

        if setting['logging'] is True:
            if 'LogChannel' in setting:
                channel = self.bot.get_channel(int(setting['LogChannel']))
                await channel.send(embed=em)
            else:
                pass
        else:
            await ctx.send(embed=em)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, id: int):

        await ctx.message.delete()
        user = discord.Object(id=id)
        banned = await self.bot.get_user_info(id)

        try:
            await ctx.guild.unban(user)

        except discord.HTTPException:
            success = False
            return

        else:
            success = True

        em = await Embeds().format_mod_embed(ctx, banned, success, 'unban')

        server = str(ctx.guild.id)
        setting = await Settings().get_server_settings(server)

        if setting['logging'] is True:
            if 'LogChannel' in setting:
                channel = self.bot.get_channel(int(setting['LogChannel']))
                await channel.send(embed=em)
            else:
                pass
        else:
            await ctx.send(embed=em)

    @commands.command(aliases=['ciao'])
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason: str = None):


        await ctx.message.delete()

        try:
            await ctx.guild.ban(user, reason=reason, delete_message_days=7)

        except discord.Forbidden:
            success = False
            return await ctx.send("Forbidden")

        except discord.HTTPException:
            success = False
            return await ctx.send("HTTPException")

        else:
            success = True

        em = await Embeds().format_mod_embed(ctx, user, success, 'ban')

        server = str(ctx.guild.id)
        setting = await Settings().get_server_settings(server)

        if setting['logging'] is True:
            if 'LogChannel' in setting:
                channel = self.bot.get_channel(int(setting['LogChannel']))
                await channel.send(embed=em)
            else:
                pass
        else:
            await ctx.send(embed=em)

    @commands.command(aliases=['clean', 'clear'])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):

        await ctx.message.delete()

        try:
            return await ctx.channel.purge(limit=amount + 1)

        except discord.HTTPException:
            pass

    @commands.command(aliases=['deafen'])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def deaf(self, ctx, user: discord.Member):
        await ctx.message.delete()

        await user.edit(deafen=True)

    @commands.command(aliases=['undeafen'])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def undeaf(self, ctx, user: discord.Member):
        await ctx.message.delete()

        await user.edit(deafen=False)

    @commands.command(aliases=['novoice'])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def vmute(self, ctx, user: discord.Member):
        await ctx.message.delete()

        await user.edit(mute=True)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def unvmute(self, ctx, user: discord.Member):
        await ctx.message.delete()

        await user.edit(mute=False)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def nick(self, ctx, user: discord.Member, name: str = None):
        await ctx.message.delete()

        await user.edit(nick=name)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def massban(self, ctx, *members: int):
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
                pass
        else:
            await ctx.send(f'{len(members)} users were banned')

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def mention(self, ctx, role: str):

        await ctx.message.delete()
        rolemention = discord.utils.get(ctx.guild.roles, name=role)

        if not rolemention.mentionable:
            await rolemention.edit(mentionable=True)

        await ctx.send(rolemention.mention)
        await rolemention.edit(mentionable=False)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def annonce(self, ctx, role: str, *, content):
        await ctx.message.delete()
        rolemention = discord.utils.get(ctx.guild.roles, name=role)

        if not rolemention.mentionable:
            await rolemention.edit(mentionable=True)

        await ctx.send("{} \n{}".format(rolemention.mention, content))
        await rolemention.edit(mentionable=False)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, role: str):
        await ctx.message.delete()
        role = discord.utils.get(ctx.guild.roles, name=role)

        for user in ctx.guild.members:
            await user.add_roles(role)
            await asyncio.sleep(1)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def removerole(self, ctx, role: str):
        await ctx.message.delete()
        role = discord.utils.get(ctx.guild.roles, name=role)

        for user in ctx.guild.members:
            await user.remove_roles(role)
            await asyncio.sleep(1)

     

def setup(bot):
    bot.add_cog(Moderation(bot))
