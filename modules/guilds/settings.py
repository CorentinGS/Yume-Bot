#  Copyright (c) 2019.
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

import asyncio

import discord
from discord.ext import commands

from modules.sql.guilddb import GuildDB
from modules.utils import checks
from modules.utils.format import Embeds


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

        guild = GuildDB.get_one(ctx.message.guild.id)

        if not guild.setup:
            await ctx.send("You must setup the bot before ! ")
            await ctx.invoke(self.setup)

        else:
            em = await Embeds().format_get_set_embed(ctx, guild.greet, guild.greet_chan, guild.blacklist, guild.logging,
                                                     guild.log_chan, guild.vip, guild.color, guild.stats_channels)
            await ctx.send(embed=em)

    @setting.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def reset(self, ctx):
        guild = GuildDB.get_one(ctx.message.guild.id)
        guild.setup = False
        GuildDB.update_guild(guild)
        await ctx.invoke(self.setup)

    @setting.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def setup(self, ctx):

        # Get guild param
        guild = GuildDB.get_one(ctx.message.guild.id)

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

        # Create logging Channel
        guild.logging = True
        overwrite = {
            ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(
                send_messages=True)
        }

        log = discord.utils.get(ctx.guild.text_channels, name="yumebot-log")
        if not isinstance(log, discord.TextChannel):
            log = await ctx.guild.create_text_channel("yumebot-log", overwrites=overwrite)

        guild.log_chan = str(log.id)

        # Welcome / Leave
        msg = await ctx.send("Do you want to activate the Welcome/Leave msg ?")

        [await msg.add_reaction(reaction) for reaction in reactions]
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
                guild.greet_chan = str(text_channel.id)
            elif reaction.emoji == '🚫':
                guild.greet = False

        # Colors

        msg = await ctx.send("Do you want to activate the Colors role ?")
        for reaction in reactions:
            await msg.add_reaction(reaction)
        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=120)
        except asyncio.TimeoutError:
            await ctx.send('👎', delete_after=3)
        else:
            if reaction.emoji == '✅':
                await msg.delete()
                guild.color = True
            elif reaction.emoji == '🚫':
                guild.color = False

        # Member stats channels
        msg = await ctx.send("Do you want to activate the member stats channels ?")
        [await msg.add_reaction(reaction) for reaction in reactions]

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=120)
        except asyncio.TimeoutError:
            await ctx.send('👎')
        else:
            if reaction.emoji == '✅':
                guild.stats_channels = True
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
                guild.stats_channels = False
                guild.count_category = 0

        guild.blacklist = False
        await msg.delete()

        # Mods & Admins role
        await ctx.send('Detecting mod and admin role...', delete_after=5)
        for role in ctx.guild.roles:
            if GuildDB.exists_in_admin(role.id, guild):
                GuildDB.remove_admin(role.id, guild)
            if role.permissions.administrator or role.permissions.manage_guild is True:
                GuildDB.set_admin(role.id, ctx.message.guild.id)
            elif role.permissions.ban_members or role.permissions.kick_members is True:
                GuildDB.set_mod(role.id, ctx.message.guild.id)
        await ctx.send('Setup is now done ! Have a good time')

        guild.setup = True
        GuildDB.update_guild(guild)

    @setting.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def role(self, ctx, value, role: discord.Role = None):
        guild = GuildDB.get_one(ctx.message.guild.id)
        if GuildDB.exists_in_admin(role.id, guild):
            GuildDB.remove_admin(role.id, guild)
        if value.lower() == 'mod':
            GuildDB.set_mod(role.id, ctx.message.guild.id)
        elif value.lower() == 'admin':
            GuildDB.set_admin(role.id, ctx.message.guild.id)
        else:
            return

        GuildDB.update_guild(guild)
        await ctx.send("Updating...", delete_after=3)

    @commands.command()
    @checks.is_owner()
    async def setting_debug(self, ctx):
        guild = GuildDB.get_one(ctx.message.guild.id)
        for role in ctx.guild.roles:
            if GuildDB.exists_in_admin(role.id, guild):
                GuildDB.remove_admin(role.id, guild)
            if role.permissions.administrator or role.permissions.manage_guild is True:
                GuildDB.set_admin(role.id, ctx.message.guild.id)
            elif role.permissions.ban_members or role.permissions.kick_members is True:
                GuildDB.set_mod(role.id, ctx.message.guild.id)

        GuildDB.update_guild(guild)
        await ctx.send("Done")

    @commands.command()
    @checks.is_owner()
    async def setting_update(self, ctx):
        for gguild in self.bot.guilds:
            guild = GuildDB.get_one(gguild.id)
            for role in gguild.roles:
                if GuildDB.exists_in_admin(role.id, guild):
                    GuildDB.remove_admin(role.id, guild)
                if role.permissions.administrator or role.permissions.manage_guild is True:
                    GuildDB.set_admin(role.id, gguild.id)
                elif role.permissions.ban_members or role.permissions.kick_members is True:
                    GuildDB.set_mod(role.id, gguild.id)
            GuildDB.update_guild(guild)
        await ctx.send("Done")

    @setting.command()
    @commands.guild_only()
    @checks.is_admin()
    async def color(self, ctx, value: bool = True):
        guild = GuildDB.get_one(ctx.message.guild.id)
        if guild.vip:
            guild.color = value
            GuildDB.update_guild(guild)
            await ctx.send("Settings updated", delete_after=3)
        else:
            await ctx.send("You're not VIP. **Our color system is VIP only.** "
                           "If you want to become VIP, feel free to **join our support discord** and ask to become VIP.")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        guildY = GuildDB.get_one(guild.id)
        if not GuildDB.guild_exists(guildY):
            GuildDB.create(guildY)
        for role in guild.roles:
            if GuildDB.exists_in_admin(role.id, guildY):
                GuildDB.remove_admin(role.id, guildY)
            if role.permissions.administrator or role.permissions.manage_guild is True:
                GuildDB.set_admin(role.id, guild.id)
            elif role.permissions.ban_members or role.permissions.kick_members is True:
                GuildDB.set_mod(role.id, guild.id)

        if guild.id == '264445053596991498':
            return
        try:
            await guild.owner.send(f"Thank you for adding the YumeBot to your guild!\n"
                                   f"In order to configure the YumeBot and to be able to use it fully"
                                   f" we ask you to make the command `--setting` in any channel of your guild **{guild.name}**"
                                   "Thank you for your understanding.\n\n"
                                   f"If you need help, do not hesitate to contact us on our discord: **invite.gg/yumenetwork**\n"
                                   f"__The YumeNetwork__")
        except discord.HTTPException:
            return


def setup(bot):
    bot.add_cog(Set(bot))
