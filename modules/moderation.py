import discord
from discord.ext import commands
import datetime
import asyncio

from modules.utils.db import Settings
from modules.utils.format import Embeds


class Moderation:

    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.command(aliases=["chut", "tg"])
    @commands.guild_only()
    #  @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, user: discord.Member, duration, *,  reason: str = None):

        await ctx.message.delete()
        server = str(ctx.guild.id)
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        setting = await Settings().get_server_settings(server)

        if not role:
            setting['muteRole'] = False
            await Settings().set_server_settings(server, setting)

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

        if 'Mute' not in setting:
            setting['Mute'] = []
        if user.id in setting['Mute']:
            return await ctx.send('This user is already muted, use {}unmute to umute him.'.format(self.bot.config['prefix']))
        setting['Mute'].append(user.id)
        await Settings().set_server_settings(server, setting)

        if setting['muteRole'] is False:
            try:
                for chan in ctx.guild.text_channels:
                    await chan.set_permissions(user, read_messages=True, send_messages=False)
            except discord.HTTPException:
                success = False
                return await ctx.send('Failed to Mute {}'.format(user))
            else:
                success = True
        else:
            try:
                await user.add_roles(role)
            except discord.HTTPException:
                success = False
                return await ctx.send('Failed to give Muted role to {}'.format(user))
            else:
                success = True

        em = await Embeds().format_mod_embed(ctx, user, success, 'mute', duration)
        await ctx.send(embed=em)

        await asyncio.sleep(time)

        if user.id in setting['Mute']:
            await ctx.invoke(self.unmute, user)
        else:
            return

    @commands.command()
    @commands.guild_only()
    #  @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, user: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        server = str(ctx.guild.id)
        setting = await Settings().get_server_settings(server)

        if not role:
            setting['muteRole'] = False
            await Settings().set_server_settings(server, setting)

        if setting['muteRole'] is False:
            try:
                for chan in ctx.guild.text_channels:
                    await chan.set_permissions(user, overwrite=None)
            except discord.HTTPException:
                success = False
                return await ctx.send('Failed to Mute {}'.format(user))
            else:
                success = True

        else:
            try:
                await user.remove_roles(role)

            except discord.HTTPException:
                success = False
                return

            else:
                success = True

        if setting['Mute']:
            if user.id not in setting['Mute']:
                return
            setting['Mute'].remove(user.id)
        await Settings().set_server_settings(server, setting)

        em = await Embeds().format_mod_embed(ctx, user, success, 'unmute')
        await ctx.send(embed=em)

    @commands.command(aliases=['out'])
    @commands.guild_only()
    #  @commands.cooldown(2, 20, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason: str = None):

        await ctx.message.delete()

        try:
            await ctx.guild.kick(user)

        except discord.Forbidden:
            success = False
            return await ctx.send('Forbidden')

        else:
            success = True

        em = await Embeds().format_mod_embed(ctx, user, success, 'kick')
        await ctx.send(embed=em)

    @commands.command(aliases=['preventban', 'preban', 'idban'])
    @commands.guild_only()
    #  @commands.cooldown(1, 10, commands.BucketType.user)
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
        await ctx.send(embed=em)

    @commands.command()
    @commands.guild_only()
    #  @commands.cooldown(2, 10, commands.BucketType.user)
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
        await ctx.send(embed=em)

    @commands.command(aliases=['ciao'])
    @commands.guild_only()
    #  @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason: str = None):

        msg = ctx.message
        moderator = ctx.message.author

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
        await ctx.send(embed=em)

    @commands.command(aliases=['clean', 'clear'])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    #  @commands.cooldown(2, 10, commands.BucketType.user)
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
    #  @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def massban(self, ctx, reason: str = None, *members: int):

        try:
            for member_id in members:
                #  user = await self.bot.get_user_info(member_id)
                await ctx.guild.ban(discord.Object(id=member_id), reason="{} - {}".format(ctx.message.author, reason))

        except Exception as e:
            success = False
            return await ctx.send(e)
        else:
            success = True

        await ctx.send(f'{len(members)} users were banned')
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(Moderation(bot))
