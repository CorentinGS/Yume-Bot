import discord
from discord.ext import commands
import json
import datetime
from itertools import cycle
import asyncio

from modules.utils.db import Settings


class Moderation:

    conf = {}

    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

        global conf
        conf = config

    @commands.command(pass_context=True, aliases=["chut", "tg"])
    @commands.guild_only()
    #@commands.cooldown(2, 10, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, user: discord.Member, duration, *,  reason: str = None):

        msg = ctx.message
        await msg.delete()
        server = str(ctx.guild.id)
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            return await ctx.send('There is no role called Muted on your server! Please add one.')

        unit = duration[-1]
        if unit == 's':
            time = int(duration[:-1])
            longunit = 'seconds'
        elif unit == 'm':
            time = int(duration[:-1]) * 60
            longunit = 'minutes'
        elif unit == 'h':
            time = int(duration[:-1]) * 3600
            longunit = 'hours'
        elif unit == 'd':
            time = int(duration[:-1]) * 86400
            longunit = 'days'
        else:
            return await ctx.send('Invalid Unit! Use `s`, `m`, `h` or `d`.')
        # await Settings().set_server_settings(server, {})
        setting = await Settings().get_server_settings(server)
        if 'Mute' not in setting:
            setting['Mute'] = []
        if user.id in setting['Mute']:
            return await ctx.send('This user is already muted, use {}unmute to umute him.'.format(self.bot.config['prefix']))
        setting['Mute'].append(user.id)
        await Settings().set_server_settings(server, setting)
        setting = await Settings().get_server_settings(server)
        try:
            await user.add_roles(role)
        except HTTPException:
            return await ctx.send('Failed to give Muted role to {}'.format(user))
        await ctx.send('**{}** has been muted for **{}**.'.format(user, duration))
        await asyncio.sleep(time)
        await ctx.invoke(self.unmute, user)

    @commands.command(pass_context=True)
    @commands.guild_only()
    #@commands.cooldown(2, 10, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, user: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            return await ctx.send('There is no role called Muted on your server! Please add one.')
        msg = ctx.message
        server = str(ctx.guild.id)
        try:
            await user.remove_roles(role)
        except discord.HTTPException:
            pass
        await msg.delete()
        setting = await Settings().get_server_settings(server)
        if setting['Mute']:
            if user.id not in setting['Mute']:
                return
            setting['Mute'].remove(user.id)
        await Settings().set_server_settings(server, setting)

        await ctx.send("**{}** has been unmuted.".format(user))

    @commands.command(pass_context=True, alises=['away'])
    @commands.guild_only()
    #@commands.cooldown(2, 20, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = None):

        msg = ctx.message
        server = ctx.guild
        moderator = ctx.message.author

        try:
            await ctx.guild.kick(member)

        except discord.Forbidden:
            return await ctx.send('Forbidden')

        embed = discord.Embed(
            title="Kick",
            description="The KickHammer stroke someone...",
            color=discord.Colour.dark_red()
        )

        embed.add_field(name="Name", value="{}#{}".format(
            member.name, member.discriminator), inline=True)
        embed.add_field(name="Created at", value=member.created_at.strftime(
            '%A - %B - %e - %g at %H:%M'), inline=True)
        embed.add_field(name="Kicked at", value=datetime.datetime.now().strftime(
            '%A - %B - %e - %g at %H:%M'), inline=True)
        embed.add_field(name="ID", value=id, inline=True)
        embed.add_field(name="Reason", value=reason, inline=True)
        embed.add_field(name="Mod", value=moderator, inline=True)
        embed.set_thumbnail(url=member.avatar_url)

        await msg.delete()
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['preventban', 'preban', 'idban'])
    @commands.guild_only()
    #@commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def hackban(self, ctx, id: int, *, reason: str = None):

        server = ctx.guild
        msg = ctx.message
        moderator = ctx.message.author
        member = discord.Object(id=id)

        try:
            await ctx.guild.ban(member)

        except discord.Forbidden:
            return await ctx.send("Forbidden")

        banned = await self.bot.get_user_info(id)

        embed = discord.Embed(
            title="Hackban",
            description="The BanHammer stroke someone...",
            color=discord.Colour.dark_red()
        )

        embed.add_field(name="Name", value="{}#{}".format(
            banned.name, banned.discriminator), inline=True)
        embed.add_field(name="Created at", value=banned.created_at.strftime(
            '%A - %B - %e - %g at %H:%M'), inline=True)
        embed.add_field(name="Banned at", value=datetime.datetime.now().strftime(
            '%A - %B - %e - %g at %H:%M'), inline=True)
        embed.add_field(name="ID", value=id, inline=True)
        embed.add_field(name="Reason", value=reason, inline=True)
        embed.add_field(name="Mod", value=moderator, inline=True)
        embed.set_thumbnail(url=banned.avatar_url)

        await msg.delete()
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.guild_only()
    #@commands.cooldown(2, 10, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, id: int):

        server = ctx.guild
        msg = ctx.message
        await msg.delete()
        moderator = ctx.message.author
        member = discord.Object(id=id)

        try:
            await ctx.guild.unban(member)

        except discord.HTTPException:
            pass


    @commands.command(pass_context=True, aliases=['ciao'])
    @commands.guild_only()
    #@commands.cooldown(2, 10, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason: str = None):

        server = ctx.guild
        msg = ctx.message
        moderator = ctx.message.author
        id = user.id

        try:
            await ctx.guild.ban(user, reason=reason, delete_message_days=7)

        except discord.Forbidden:
            return await ctx.send("Forbidden")

        except discord.HTTPException:
            return await ctx.send("HTTPException")

        embed = discord.Embed(
            title="Ban",
            description="The BanHammer stroke someone...",
            color=discord.Colour.dark_red()
        )

        embed.add_field(name="Name", value="{}#{}".format(
            user.name, user.discriminator), inline=True)
        embed.add_field(name="Created at", value=user.created_at.strftime(
            '%A - %B - %e - %g at %H:%M'), inline=True)
        embed.add_field(name="Banned at", value=datetime.datetime.now().strftime(
            '%A - %B - %e - %g at %H:%M'), inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Reason", value=reason, inline=True)
        embed.add_field(name="Mod", value=moderator, inline=True)
        embed.set_thumbnail(url=user.avatar_url)

        await msg.delete()
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['clean', 'clear'])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    #@commands.cooldown(2, 10, commands.BucketType.user)
    async def purge(self, ctx, amount: int):

        msg = ctx.message

        try:
            await msg.delete()
            return await ctx.channel.purge(limit=amount + 1)

        except discord.HTTPException:
            pass


    @commands.command(pass_context=True, aliases=['deafen'])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def deaf(self, ctx, user: discord.Member):
        msg = ctx.message
        await msg.delete()

        await user.edit(deafen = True)

    @commands.command(pass_context=True, aliases= ['undeafen'])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def undeaf(self, ctx, user: discord.Member):
        msg = ctx.message
        await msg.delete()

        await user.edit(deafen = False)

    @commands.command(pass_context=True, aliases= ['novoice'])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def vmute(self, ctx, user: discord.Member):
        msg = ctx.message
        await msg.delete()

        await user.edit(mute = True)


    @commands.command(pass_context=True)
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def unvmute(self, ctx, user: discord.Member):
        msg = ctx.message
        await msg.delete()

        await user.edit(mute = False)


    @commands.command(pass_context=True)
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def nick(self, ctx, user: discord.Member, name: str = None):
        msg = ctx.message
        await msg.delete()

        await user.edit(nick = name)

    @commands.command(pass_context=True)
    @commands.guild_only()
    #@commands.cooldown(2, 10, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def massban(self, ctx, reason: str = None, *members: int):

        try:
            for member_id in members:
                user = await self.bot.get_user_info(member_id)
                await ctx.guild.ban(discord.Object(id=member_id), reason="{} - {}".format(ctx.message.author, reason))
                # await ctx.send("{user.name}#{user.discriminator} has been banned")
                await ctx.send("Banned")
            return
        except Exception as e:
            return await ctx.send(e)


    async def on_member_join(self, member):
        server = str(member.guild.id)
        setting = await Settings().get_server_settings(server)
        if 'Mute' in setting:
            if member.id in setting['Mute']:
                role = discord.utils.get(member.guild.roles, name="Muted")
                if role:
                    await member.add_roles(role)


def setup(bot):
    bot.add_cog(Moderation(bot, bot.config))
