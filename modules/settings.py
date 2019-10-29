import asyncio

import discord
from discord.ext import commands

from modules.utils import checks
from modules.utils.db import Settings
from modules.utils.format import Embeds
from modules.utils.setup import GuildY


class Set(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.group()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def setting(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.get)

    @setting.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def get(self, ctx):
        await ctx.message.delete()
        guild = GuildY(ctx.message.guild)
        await guild.get()

        if not guild.setup:
            await ctx.send("You must setup the bot before ! ")
            await ctx.invoke(self.setup)

        else:
            em = await Embeds().format_get_set_embed(ctx, guild.greet, guild.greet_channel, guild.bl, guild.logging,
                                                     guild.log_channel, guild.automod, guild.members_count, guild.vip)
            await ctx.send(embed=em)

    @setting.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def reset(self, ctx):
        guild = GuildY(ctx.message.guild)
        await guild.set()
        await ctx.invoke(self.setup)

    @setting.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def setup(self, ctx):

        # Get guild param
        guild = GuildY(ctx.message.guild)
        await guild.get()

        # Create check
        def check(reaction, user):
            return (user == ctx.message.author) and str(reaction.emoji)

        def msgcheck(m):
            return m.author == ctx.message.author

        # Check if already setup
        if guild.setup:
            return await ctx.send("The setup has already been done. "
                                  "If you want to restore it you should use : **--setting reset**")

        reactions = ['✅', '🚫']  # Store reactions

        await ctx.send("Hey ! Let's setup your server ;) ", delete_after=3)

        # VIP

        glob = await Settings().get_glob_settings()

        if ctx.guild.owner in glob['VIP'] or ctx.guild.id in glob['VIP']:
            guild.vip = True
            guild.automod = True
            await guild.set()

        # Create logging Channel
        guild.logging = True
        overwrite = {
            ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(
                send_messages=True)
        }

        log = await ctx.guild.create_text_channel("YumeBot-log", overwrites=overwrite)
        guild.log_channel = str(log.id)

        # Welcome / Leave
        msg = await ctx.send("Do you want to activate the Welcome/Leave msg ?")
        for reaction in reactions:
            await msg.add_reaction(reaction)

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=120)
        except asyncio.TimeoutError:
            await ctx.send('👎', delete_after=3)
        else:
            if reaction.emoji == '✅':
                await msg.delete()
                msg = await ctx.send('Please mention a Channel !\nEx: `#general`')
                try:
                    m = await self.bot.wait_for('message', timeout=120, check=msgcheck)
                except asyncio.TimeoutError:
                    return await ctx.send('👎', delete_after=3)
                try:
                    text_channel = m.channel_mentions[0]
                except IndexError:
                    text_channel = ctx.message.channel

                await msg.delete()
                guild.greet = True
                guild.greet_channel = str(text_channel.id)
            elif reaction.emoji == '🚫':
                guild.greet = False

        await guild.set()

        # Member stats channels
        msg = await ctx.send("Do you want to activate the member stats channels ?")
        for reaction in reactions:
            await msg.add_reaction(reaction)

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=120)
        except asyncio.TimeoutError:
            await ctx.send('👎')
        else:
            if reaction.emoji == '✅':
                guild.members_count = True
                overwrite = {
                    ctx.guild.default_role: discord.PermissionOverwrite(connect=False),
                }

                category = await ctx.guild.create_category_channel("Stats", overwrites=overwrite)
                guild.count_category = str(category.id)

                await ctx.guild.create_voice_channel(f'Users : {len(ctx.guild.members)}', overwrites=overwrite,
                                                     category=category)
                bots = []
                for user in ctx.guild.members:
                    if user.bot is True:
                        bots.append(user)
                await ctx.guild.create_voice_channel(f'Bots : {len(bots)}', overwrites=overwrite, category=category)
                await ctx.guild.create_voice_channel(f'Members : {len(ctx.guild.members) - len(bots)}',
                                                     overwrites=overwrite, category=category)

            elif reaction.emoji == '🚫':
                guild.members_count = False

        guild.bl = True
        await guild.set()
        await msg.delete()

        # Mods & Admins role
        await ctx.send('Detecting mod and admin role...', delete_after=5)
        for role in ctx.guild.roles:
            if role.permissions.administrator or role.permissions.manage_guild is True:
                guild.admins.append(str(role.id))
            elif role.permissions.ban_members or role.permissions.kick_members is True:
                guild.mods.append(str(role.id))
        await ctx.send('Setup is now done ! Have a good time')

        guild.setup = True
        await guild.set()

    @setting.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def role(self, ctx, value, role: discord.Role = None):
        guild = GuildY(ctx.message.guild)
        await guild.get()
        if value.lower() == 'mod':
            guild.mods.append(str(role.id))
        elif value.lower() == 'admin':
            guild.admins.append(str(role.id))
        else:
            return

        await guild.set()
        await ctx.send("Updating...", delete_after=3)

    @commands.command()
    @checks.is_owner()
    async def setting_debug(self, ctx):
        guildy = GuildY(ctx.guild)

        for role in ctx.guild.roles:
            if role.permissions.administrator or role.permissions.manage_guild is True:
                guildy.admins.append(str(role.id))
            elif role.permissions.ban_members or role.permissions.kick_members is True:
                guildy.mods.append(str(role.id))

        await guildy.set()

        await ctx.send("Done")

    @setting.command()
    @commands.guild_only()
    @checks.is_admin()
    async def automod(self, ctx, value: bool = True):
        guild = GuildY(ctx.guild)
        await guild.get()

        glob = await Settings().get_glob_settings()

        if ctx.guild.owner in glob['VIP'] or ctx.guild.id in glob['VIP'] or ctx.author.id in glob['VIP']:
            guild.vip = True
            guild.automod = value
            await guild.set()
            await ctx.send("Settings updated", delete_after=3)
        else:
            await ctx.send("You're not VIP. **Our automod system is VIP only.** "
                           "If you want to become VIP, feel free to **join our support discord** and ask to become VIP.")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        guildy = GuildY(guild)

        for role in guild.roles:
            if role.permissions.administrator or role.permissions.manage_guild is True:
                guildy.admins.append(str(role.id))
            elif role.permissions.ban_members or role.permissions.kick_members is True:
                guildy.mods.append(str(role.id))

        await guildy.set()
        if guild.id == '264445053596991498':
            return
        try:
            await guild.owner.send(f"Thank you for adding the YumeBot to your guild!\n"
                                   f"In order to configure the YumeBot and to be able to use it fully"
                                   f" we ask you to make the command `--setting` in any lounge of your guild **{guild.name}**"
                                   "Thank you for your understanding.\n\n"
                                   f"If you need help, do not hesitate to contact us on our discord: **https://discord.gg/3BKgvpp**\n"
                                   f"__The YumeNetwork__")
        except discord.HTTPException:
            return


def setup(bot):
    bot.add_cog(Set(bot))
