import asyncio

import discord
from discord.ext import commands

from modules.utils import checks
from modules.utils.db import Settings
from modules.utils.format import Embeds
from modules.utils.setup import Setup


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
        await ctx.message.delete()
        vip = False

        set = await Settings().get_server_settings(str(ctx.guild.id))
        glob = await Settings().get_glob_settings()

        if ctx.guild.owner in glob['VIP'] or ctx.guild.id in glob['VIP']:
            vip = True

        if not 'Setup' in set:
            set['Setup'] = False

        await Settings().set_server_settings(str(ctx.guild.id), set)

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

            em = await Embeds().format_get_set_embed(ctx, greet, greetchannel, blacklist, logging, logchannel, automod, display, vip)
            await ctx.send(embed=em)

    @setting.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def reset(self, ctx):
        await Setup().new_guild(ctx.message.guild.id)
        await ctx.invoke(self.setup)

    @setting.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx):

        guild = ctx.message.guild
        set = await Settings().get_server_settings(str(guild.id))

        # glob = await Settings().get_glob_settings()

        def check(reaction, user):
            return (user == ctx.message.author) and str(reaction.emoji)

        def msgcheck(m):
            return m.author == ctx.message.author

        if not "Setup" in set:
            set['Setup'] = False

        if set['Setup'] is True:
            return await ctx.send("The setup has already been done. "
                                  "If you want to restore it you should use : **--setting reset**")

        reactions = ['✅', '🚫']
        await ctx.send("Hey ! Let's setup your server ;) ", delete_after=3)

        await Setup().new_guild(guild.id)

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
                await Setup().new_guild(guild.id)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        set = await Settings().get_server_settings(str(guild.id))
        await Setup().new_guild(guild.id)

        for role in guild.roles:
            if role.permissions.administrator or role.permissions.manage_guild is True:
                set['Admins'].append(str(role.id))
            elif role.permissions.ban_members or role.permissions.kick_members is True:
                set['Mods'].append(str(role.id))

        await Settings().set_server_settings(str(guild.id), set)

        await guild.owner.send(f"Hi ! To use the bot you should use this command in any channel of your guild {guild.name} :\n**--setting setup**")


def setup(bot):
    bot.add_cog(Set(bot))
