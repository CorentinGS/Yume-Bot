import asyncio
import datetime

import discord
from discord.ext import commands

from modules.utils import checks
from modules.utils.db import Settings
from modules.utils.format import Embeds


class Set(commands.Cog):

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
    async def get(self, ctx):
        guild = ctx.message.guild
        set = await Settings().get_server_settings(str(guild.id))

        if not 'Setup' in set:
            set['Setup'] = False

        await Settings().set_server_settings(str(guild.id), set)

        if set['Setup'] is False:
            await ctx.send("You must setup the bot before ! Use **--setting setup**")

        else:
            greet = set['Greet']
            blacklist = set['bl']
            logging = set['logging']
            greetchannel = set['GreetChannel']
            logchannel = set['LogChannel']
            automod = set['automod']
            display = set['Display']

            em = await Embeds().format_get_set_embed(ctx, guild, greet, greetchannel, blacklist, logging, logchannel, automod, display)
            msg = await ctx.send(embed=em)

    @setting.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def reset(self, ctx):
        guild = ctx.message.guild
        set = await Settings().get_server_settings(str(guild.id))
        if not "Setup" in set:
            set["Setup"] is False

        await Settings().set_server_settings(str(guild.id), set)

        if set['Setup'] is False:
            return await ctx.send("You must setup your server before reseting it...")

        else:
            set['Greet'] = False
            set['bl'] = False
            set['logging'] = False
            set['GreetChannel'] = None
            set['LogChannel'] = None
            set['automod'] = False
            set['Mute'] = []
            set['Display'] = False
            set['category'] = None
            set['Admins'] = []
            set['Mods'] = []
            set['Setup'] = False

        await Settings().set_server_settings(str(guild.id), set)
        await ctx.invoke(self.setup)

    @setting.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx):
        guild = ctx.message.guild
        set = await Settings().get_server_settings(str(guild.id))
        glob = await Settings().get_glob_settings()

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji)

        def msgcheck(m):
            if m.author == ctx.message.author:
                return True
            else:
                return False

        if not "Setup" in set:
            set['Setup'] = False

        if set['Setup'] is True:
            return await ctx.send("The setup has already been done. If you want to restore it you should use : **--setting reset**")
        reactions = ['✅', '🚫']
        await ctx.send("Hey ! Let's setup your server ;) ", delete_after=3)

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

        set['logging'] = True

        overwrite = {
            ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(
                send_messages=True)
        }
        log = await ctx.guild.create_text_channel("YumeBot-log", overwrites=overwrite)
        set['LogChannel'] = str(log.id)

        await Settings().set_server_settings(str(guild.id), set)

        msg = await ctx.send("Do you want to activate the Welcome/Leave msg ?")
        for reaction in reactions:
            await msg.add_reaction(reaction)

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=120)

        except asyncio.TimeoutError:
            await ctx.send('👎', delete_after=3)

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

        msg = await ctx.send("Do you want to activate the member stats channels ?")
        for reaction in reactions:
            await msg.add_reaction(reaction)

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=120)

        except asyncio.TimeoutError:
            await ctx.send('👎')

        else:
            if reaction.emoji == '✅':
                set['Display'] = True
                overwrite = {
                    ctx.guild.default_role: discord.PermissionOverwrite(connect=False),
                }

                category = await ctx.guild.create_category_channel("Stats", overwrites=overwrite)

                set['category'] = str(category.id)
                await Settings().set_server_settings(str(guild.id), set)

                await ctx.guild.create_voice_channel(f'Users : {len(ctx.guild.members)}', overwrites=overwrite, category=category)
                bots = []
                for user in ctx.guild.members:
                    if user.bot is True:
                        bots.append(user)
                await ctx.guild.create_voice_channel(f'Bots : {len(bots)}', overwrites=overwrite, category=category)
                await ctx.guild.create_voice_channel(f'Members : {len(ctx.guild.members) - len(bots)}', overwrites=overwrite, category=category)

            elif reaction.emoji == '🚫':
                set['Display'] = False

        await msg.delete()
        set['bl'] = True

        await ctx.send('Detecting mod and admin role...', delete_after=5)
        for role in guild.roles:
            if role.permissions.administrator or role.permissions.manage_guild is True:
                set['Admins'].append(str(role.id))
            elif role.permissions.ban_members or role.permissions.kick_members is True:
                set['Mods'].append(str(role.id))
        await ctx.send('Setup is now done ! Have a good time')

        set['Setup'] = True
        await Settings().set_server_settings(str(guild.id), set)

    @setting.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def role(self, ctx, value, role: discord.Role = None):
        guild = ctx.message.guild
        set = await Settings().get_server_settings(str(guild.id))

        if value.lower() == 'mod':
            set['Mods'].append(str(role.id))
        elif value.lower() == 'admin':
            set['Admins'].append(str(role.id))

        await Settings().set_server_settings(str(guild.id), set)

    @setting.command(hidden=True)
    @checks.is_owner()
    async def update(self, ctx):
        for guild in self.bot.guilds:
            set = await Settings().get_server_settings(str(guild.id))
            if not "Setup" in set:
                set["Setup"] = False
                set['Greet'] = False
                set['bl'] = False
                set['logging'] = False
                set['GreetChannel'] = None
                set['LogChannel'] = None
                set['automod'] = False
                set['Mute'] = []
                set['Display'] = False
                set['category'] = None
                set['Admins'] = []
                set['Mods'] = []
                set['Setup'] = False
                set['levels'] = {}

            await Settings().set_server_settings(str(guild.id), set)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        set = await Settings().get_server_settings(str(guild.id))
        if not "Setup" in set:
            set["Setup"] = False
            set['Greet'] = False
            set['bl'] = False
            set['logging'] = False
            set['GreetChannel'] = None
            set['LogChannel'] = None
            set['automod'] = False
            set['Mute'] = []
            set['Display'] = False
            set['category'] = None
            set['Admins'] = []
            set['Mods'] = []
            set['Setup'] = False
            set['levels'] = {}

        await Settings().set_server_settings(str(guild.id), set)      


def setup(bot):
    bot.add_cog(Set(bot))
