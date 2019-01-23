import asyncio
import datetime

import discord
from discord.ext import commands

from modules.utils import checks
from modules.utils.db import Settings
from modules.utils.format import Embeds


class Set:

    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.group()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def setting(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.get)

    @setting.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def role(self, ctx, value, role: discord.Role=None):
        guild = ctx.message.guild
        set = await Settings().get_server_settings(str(guild.id))

        if value.lower() == 'mod':
            set['Mods'].append(str(role.id))
        elif value.lower() == 'admin':
            set['Admins'].append(str(role.id))
        elif value.lower() == 'auto':
            for role in guild.roles:
                if role.permissions.administrator or role.permissions.manage_guild is True:
                    set['Admins'].append(str(role.id))
                elif role.permissions.ban_members or role.permissions.kick_members is True:
                    set['Mods'].append(str(role.id))

        await Settings().set_server_settings(str(guild.id), set)

    @setting.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx):
        guild = ctx.message.guild
        set = await Settings().get_server_settings(str(guild.id))
        glob = await Settings().get_glob_settings()
        reactions = ['✅', '🚫']
        await ctx.send("Hey ! Let's setup your server ;) ", delete_after=3)
        msg = await ctx.send("Do you want to activate the logging  ?")
        for reaction in reactions:
            await msg.add_reaction(reaction)

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji)

        def msgcheck(m):
            if m.author == ctx.message.author:
                return True
            else:
                return False

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=240)

        except asyncio.TimeoutError:
            await ctx.send('👎')

        else:
            if reaction.emoji == '✅':
                set['logging'] = True
                overwrite = {
                    ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False),
                    ctx.guild.me: discord.PermissionOverwrite(
                        send_messages=True)
                }
                log = await ctx.guild.create_text_channel("YumeBot-log", overwrites=overwrite)
                set['LogChannel'] = str(log.id)
            elif reaction.emoji == '🚫':
                set['logging'] = False

        await ctx.send("Ok ! ", delete_after=3)
        msg = await ctx.send("Do you want to activate the Welcome/Leave msg ?")

        for reaction in reactions:
            await msg.add_reaction(reaction)

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=120)

        except asyncio.TimeoutError:
            await ctx.send('👎')

        else:
            if reaction.emoji == '✅':
                set['Greet'] = True
                await msg.delete()
                if set['GreetChannel'] is None:
                    msg = await ctx.send('Please name a Channel !')
                    m = await self.bot.wait_for('message', timeout=120, check=msgcheck)
                    text_channel = m.channel_mentions[0]
                    await msg.delete()
                    set['GreetChannel'] = str(text_channel.id)
            elif reaction.emoji == '🚫':
                set['Greet'] = False

        await ctx.send("Ok ! ", delete_after=3)
        msg = await ctx.send("Do you want to activate the member stats channels ?")
        for reaction in reactions:
            await msg.add_reaction(reaction)

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=120)

        except asyncio.TimeoutError:
            await ctx.send('👎')

        else:
            if reaction.emoji == '✅':
                arg = True

            elif reaction.emoji == '🚫':
                arg = False

            await msg.delete()
            await ctx.invoke(self.display, arg)

        await ctx.send("Ok ! ", delete_after=3)
        msg = await ctx.send("Do you want to activate the blacklist ?")

        for reaction in reactions:
            await msg.add_reaction(reaction)

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=120)

        except asyncio.TimeoutError:
            await ctx.send('👎')

        else:
            if reaction.emoji == '✅':
                arg = True

            elif reaction.emoji == '🚫':
                arg = False

            await msg.delete()
            set['bl'] = arg

        await ctx.send("Ok ! ", delete_after=3)

        if ctx.message.author in glob["VIP"]:
            msg = await ctx.send("Do you want to activate the automoderation ?")

            for reaction in reactions:
                await msg.add_reaction(reaction)

            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=120)

            except asyncio.TimeoutError:
                await ctx.send('👎')

            else:
                if reaction.emoji == '✅':
                    arg = True

                elif reaction.emoji == '🚫':
                    arg = False

                set['automod'] = arg
                await msg.delete()

        await ctx.send('Setup is now done ! Have a good time')

        await Settings().set_server_settings(str(guild.id), set)

    @setting.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def get(self, ctx):
        guild = ctx.message.guild
        set = await Settings().get_server_settings(str(guild.id))

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji)

        if not 'Greet' in set:
            set['Greet'] = False
        if not 'bl' in set:
            set['bl'] = False
        if not 'logging' in set:
            set['logging'] = False
        if not 'GreetChannel' in set:
            set['GreetChannel'] = None
        if not 'LogChannel' in set:
            set['LogChannel'] = None
        if not 'automod' in set:
            set['automod'] = False
        if not 'Mute' in set:
            set['Mute'] = []
        if not 'Display' in set:
            set['Display'] = False
        if not 'category' in set:
            set['category'] = None
        if not 'Admins' in set:
            set['Admins'] = []
        if not 'Mods' in set:
            set['Mods'] = []

        await Settings().set_server_settings(str(guild.id), set)

        greet = set['Greet']
        blacklist = set['bl']
        logging = set['logging']
        greetchannel = set['GreetChannel']
        logchannel = set['LogChannel']
        automod = set['automod']
        display = set['Display']

        em = await Embeds().format_get_set_embed(ctx, guild, greet, greetchannel, blacklist, logging, logchannel, automod, display)

        reactions = ["✏", '❌']

        msg = await ctx.send(embed=em)

        for reaction in reactions:
            await msg.add_reaction(reaction)

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=240)

        except asyncio.TimeoutError:
            await ctx.send('👎', delete_after=10)

        else:
            if reaction.emoji == '✏':
                await msg.clear_reactions()
                await msg.delete()
                await ctx.invoke(self.edit)
            if reaction.emoji == '❌':
                await msg.clear_reactions()
                await msg.delete()
                return

    @setting.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def edit(self, ctx):
        vip = False

        guild = ctx.message.guild
        set = await Settings().get_server_settings(str(guild.id))
        em = await Embeds().format_set_embed(ctx, guild, 'setting', vip)
        glob = await Settings().get_glob_settings()

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji)

        def msgcheck(m):
            if m.author == ctx.message.author:
                return True
            else:
                return False

        msg = await ctx.send(embed=em)
        reactions = ['🇬', '⛔', '🖊', '🔨', '❌']
        for reaction in reactions:
            await msg.add_reaction(reaction)

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)

        except asyncio.TimeoutError:
            await ctx.send('👎')

        else:

            if reaction.emoji == '🔨':
                await msg.clear_reactions()
                if ctx.message.author in glob["VIP"]:
                    vip = True
                em = await Embeds().format_set_embed(ctx, guild, 'automenu', vip)
                await msg.edit(embed=em)
                reactions = ['✅', '🚫', '❌']
                if vip is True:
                    reactions.extend(['⛔'])
                for reaction in reactions:
                    await msg.add_reaction(reaction)

                try:
                    reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)

                except asyncio.TimeoutError:
                    await ctx.send('👎', delete_after=10)

                else:
                    if reaction.emoji == '✅':
                        set["automod"] = True
                        await msg.delete()
                        await Settings().set_server_settings(str(guild.id), set)
                        await ctx.invoke(self.setting)
                    elif reaction.emoji == '🚫':
                        set['automod'] = False
                        await msg.delete()
                        await Settings().set_server_settings(str(guild.id), set)
                        await ctx.invoke(self.setting)
                    elif reaction.emoji == '⛔':
                        await msg.delete()
                        await ctx.send("Not ready ! Ccoming Soon")
                        await ctx.invoke(self.setting)
                    elif reaction.emoji == '❌':
                        await msg.delete()
                        return

            elif reaction.emoji == '🖊':
                if ctx.message.author in glob["VIP"]:
                    vip = True

                await msg.clear_reactions()
                em = await Embeds().format_set_embed(ctx, guild, 'loggingmenu', vip)
                await msg.edit(embed=em)
                reactions = ['📋', '🆓', '❌']
                '''
                    if vip is True:
                        reactions.extend(['🎬'])
                    '''
                for reaction in reactions:
                    await msg.add_reaction(reaction)
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=120)

                except asyncio.TimeoutError:
                    await ctx.send('👎')

                else:
                    if reaction.emoji == '📋':
                        arg = "on"
                        await ctx.invoke(self.logging, arg)
                        await msg.delete()
                        await ctx.invoke(self.setting)
                    elif reaction.emoji == '🆓':
                        arg = 'off'
                        await ctx.invoke(self.logging, arg)
                        await msg.delete()
                    elif reaction.emoji == '❌':
                        await msg.delete()
                        return
            elif reaction.emoji == '⛔':
                await msg.clear_reactions()
                em = await Embeds().format_set_embed(ctx, guild, 'blacklistmenu', vip)
                await msg.edit(embed=em)
                reactions = ['🚫', '🔓', '❌']
                for reaction in reactions:
                    await msg.add_reaction(reaction)
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)

                except asyncio.TimeoutError:
                    await ctx.send('👎')

                else:
                    if reaction.emoji == '🚫':
                        arg = True
                        await ctx.invoke(self.bl, arg)
                        await msg.delete()
                        await ctx.invoke(self.setting)
                    elif reaction.emoji == '🔓':
                        arg = False
                        await ctx.invoke(self.bl, arg)
                        await msg.delete()
                        await ctx.invoke(self.setting)
                    elif reaction.emoji == '❌':
                        await msg.delete()
                        return

            elif reaction.emoji == '🇬':
                await msg.clear_reactions()
                em = await Embeds().format_set_embed(ctx, guild, 'greetmenu', vip)
                await msg.edit(embed=em)
                reactions = ['❔', '📜', '❌']
                for reaction in reactions:
                    await msg.add_reaction(reaction)
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)

                except asyncio.TimeoutError:
                    await ctx.send('👎')

                else:
                    if reaction.emoji == '❔':
                        await msg.delete()
                        await ctx.send('Please name a Channel !')
                        m = await self.bot.wait_for('message', timeout=60.0, check=msgcheck)
                        text_channel = m.channel_mentions[0]
                        await ctx.invoke(self.greetchannel, text_channel)
                        await ctx.invoke(self.setting)
                    elif reaction.emoji == '📜':
                        await ctx.invoke(self.greet)
                        await msg.delete()
                        if set['GreetChannel'] is None:
                            await ctx.send('Please name a Channel !')
                            m = await self.bot.wait_for('message', timeout=60.0, check=msgcheck)
                            text_channel = m.channel_mentions[0]
                            await ctx.invoke(self.greetchannel, text_channel)
                        else:
                            await ctx.invoke(self.setting)
                    elif reaction.emoji == '❌':
                        await msg.delete()
                        return

            elif reaction.emoji == '❌':
                await msg.delete()
                return


# TODO : Refaire le system de channels et les proposer automatiquement quand on active !


    @setting.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def logging(self, ctx, arg: str = None):
        server = str(ctx.guild.id)
        set = await Settings().get_server_settings(server)
        if arg.lower().startswith('on'):
            set['logging'] = True
            channel = self.bot.get_channel(int(set['LogChannel']))
            if set['LogChannel'] is None or not channel:
                overwrite = {
                    ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False),
                    ctx.guild.me: discord.PermissionOverwrite(
                        send_messages=True)
                }
                log = await ctx.guild.create_text_channel("YumeBot-log", overwrites=overwrite)
                set['LogChannel'] = str(log.id)

        elif arg.lower().startswith('off'):
            set['logging'] = False

        await Settings().set_server_settings(server, set)

        await ctx.send('OK !', delete_after=5)

    @setting.command()
    @commands.has_permissions(administrator=True)
    async def bl(self, ctx, arg: bool = False):
        server = str(ctx.guild.id)
        set = await Settings().get_server_settings(server)
        if arg is True:
            set['bl'] = True
        else:
            set['bl'] = False
        await Settings().set_server_settings(server, set)

        await ctx.send('OK !', delete_after=5)

    @setting.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def greetchannel(self, ctx, channel: discord.TextChannel):
        server = str(ctx.guild.id)
        set = await Settings().get_server_settings(server)

        if not channel:
            return await ctx.send('Invalid Channel')

        else:
            set['GreetChannel'] = str(channel.id)

        await Settings().set_server_settings(server, set)

        await ctx.send('OK !', delete_after=5)

    @setting.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def greet(self, ctx):
        server = str(ctx.guild.id)
        set = await Settings().get_server_settings(server)
        if set['Greet'] is True:
            set['Greet'] = False
        else:
            set['Greet'] = True

        await Settings().set_server_settings(server, set)

        await ctx.send('OK !', delete_after=5)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def display(self, ctx, arg: bool = True):
        server = str(ctx.guild.id)
        set = await Settings().get_server_settings(server)

        set['Display'] = arg

        if arg is True:
            overwrite = {
                ctx.guild.default_role: discord.PermissionOverwrite(connect=False),
            }

            category = await ctx.guild.create_category_channel("Stats", overwrites=overwrite)
            set['category'] = str(category.id)
            await Settings().set_server_settings(server, set)

            await ctx.guild.create_voice_channel(f'Users : {len(ctx.guild.members)}', overwrites=overwrite, category=category)
            bots = []
            for user in ctx.guild.members:
                if user.bot is True:
                    bots.append(user)
            await ctx.guild.create_voice_channel(f'Bots : {len(bots)}', overwrites=overwrite, category=category)
            await ctx.guild.create_voice_channel(f'Members : {len(ctx.guild.members) - len(bots)}', overwrites=overwrite, category=category)

        await Settings().set_server_settings(server, set)


def setup(bot):
    bot.add_cog(Set(bot))
