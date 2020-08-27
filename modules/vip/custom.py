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
import random
from datetime import datetime

import discord
from discord.ext import commands, tasks

from modules.sql.anondb import AnonDB
from modules.sql.networkdb import NetworkDB
from modules.sql.privatedb import PrivateDB
from modules.utils import checks


class Custom(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    """
    @commands.command()
    @checks.is_owner()
    @commands.guild_only()
    async def network_set(self, ctx, channel: discord.TextChannel = None):
        if not channel:
            channel = ctx.channel
        permissions: discord.Permissions = channel.permissions_for(ctx.guild.me)
        if not (
                permissions.read_messages or permissions.send_messages
                or permissions.manage_webhooks or permissions.manage_messages):
            return await ctx.send("I don't have enough permissions !"
                                  " Please be sure to give me the following permissions :\n"
                                  "**read_messages**, **send_messages**, **manage_webhooks**, **manage_messages**")
        NetworkDB.set_channel(channel.id, ctx.guild.id)
        await channel.create_webhook(name="Network")
        await channel.send(f"This room is now linked to the network.")

    @commands.command()
    @checks.is_admin()
    @commands.guild_only()
    async def network_unset(self, ctx):
        NetworkDB.delete_channel(ctx.guild.id)
        await ctx.send("Network features is now unset !")

    @commands.command()
    @checks.is_owner()
    @commands.guild_only()
    async def network_block(self, ctx, user_id: int):
        NetworkDB.block_user(user_id)
        await ctx.send("User has been blocked")

    @commands.command()
    @checks.is_owner()
    @commands.guild_only()
    async def network_unblock(self, ctx, user_id: int):
        NetworkDB.unblock_user(user_id)
        await ctx.send("User has been unblocked")

    @commands.Cog.listener()
    async def on_message(self, message):
        return

        author = message.author
        if not NetworkDB.is_linked(message.channel.id):
            return
        if author.bot or not isinstance(author, discord.Member):
            return
        if NetworkDB.is_blocked(author.id):
            return
        msg = message.clean_content
        if "discord.gg" in msg or msg.startswith("--"):
            return
        msg = msg.replace('@everyone', '@\u200beveryone').replace('@here', '@\u200bhere')
        channels = NetworkDB.get_all_linked_channels()
        for chan in channels:
            if chan["chan"] == message.channel.id:
                continue
            try:
                channel = self.bot.get_channel(chan["chan"])
            except discord.NotFound:
                continue
            if isinstance(channel, discord.TextChannel):
                webhooks = await channel.webhooks()
                if not webhooks:
                    continue
                else:
                    webhook = webhooks[0]

                await webhook.send(content=msg,
                                   username="{} - {}".format(message.author.name, message.author.id),
                                   avatar_url=message.author.avatar_url, wait=True)


    @commands.group()
    async def anon(self, ctx):
        return

    @anon.command()
    @checks.is_admin()
    @commands.guild_only()
    async def set(self, ctx, channel: discord.TextChannel = None):
        if not channel:
            channel = ctx.channel
        permissions: discord.Permissions = channel.permissions_for(ctx.guild.me)
        if not (
                permissions.read_messages or permissions.send_messages
                or permissions.manage_webhooks or permissions.manage_messages):
            return await ctx.send("I don't have enough permissions !"
                                  " Please be sure to give me the following permissions :\n"
                                  "**read_messages**, **send_messages**, **manage_webhooks**, **manage_messages**")
        AnonDB.set_channel(ctx.guild.id, channel.id)
        await channel.create_webhook(name="Anon")
        msg = await channel.send(f"This room is now ready to receive anonymous messages."
                                 f"To send messages in this room, just do the following command as a private message:"
                                 f" ```--anon send {ctx.guild.id} Your text```")
        await msg.pin()

    @anon.command()
    @checks.is_admin()
    @commands.guild_only()
    async def remove(self, ctx):
        if AnonDB.is_setup(ctx.guild.id):
            AnonDB.unset_channel(ctx.guild.id)
            await ctx.send("Anon features is now unset !")
        else:
            await ctx.send("Anon features isn't set")

    @anon.command()
    @checks.is_mod()
    @commands.guild_only()
    async def block(self, ctx, message_id):
        message = AnonDB.get_message(message_id)
        if not message:
            await ctx.send("I can't find this message")
        AnonDB.block_anon(message["user_id"], message['guild_id'])
        await ctx.send("The anon author of this message has been blocked")

    @anon.command()
    @checks.is_mod()
    @commands.guild_only()
    async def unblock(self, ctx, user: discord.Member):
        AnonDB.unblock_anon(user.id, ctx.guild.id)
        await ctx.send("{} has been unblocked".format(user.display_name))

    @anon.command()
    @checks.is_admin()
    @commands.guild_only()
    async def whois(self, ctx, message_id):
        message = AnonDB.get_message(message_id)
        if not message:
            await ctx.send("I can't find this message")
        try:
            user: discord.User = await self.bot.fetch_user(message['user_id'])
        except discord.NotFound:
            await ctx.send("We couldn't find the author if this message...")
            return
        else:
            await ctx.send(
                "The anon author of this message is {}#{} - `{}`".format(user.name, user.discriminator, user.id))

    @anon.command()
    @commands.cooldown(2, 30, commands.BucketType.user)
    async def send(self, ctx, guild_id: int, *, msg: str):
        if not isinstance(ctx.message.channel, discord.DMChannel):
            return await ctx.send("This command has to be send in DM")
        setup = AnonDB.is_setup(guild_id)
        if not setup:
            return await ctx.send("This guild hasn't activate this feature yet !")
        if not AnonDB.is_author(ctx.author.id, guild_id):
            AnonDB.set_author(user_id=ctx.author.id, guild_id=guild_id)
        blocked = AnonDB.is_blocked(ctx.author.id, guild_id)
        if blocked:
            return await ctx.send(
                "Sorry, but it seems you're not allowed to use the anon command anymore. If you think this is an error,"
                " please contact the guild administrator and ask them to unlock your access.")
        anon = AnonDB.get_channel(guild_id)
        try:
            guild: discord.Guild = self.bot.get_guild(guild_id)
            chan: discord.TextChannel = guild.get_channel(anon["channel_id"])
        except discord.HTTPException:
            return await ctx.send(
                "Sorry, but I couldn't find the anonymous message room. If you think this is an error, "
                "please contact the guild administrator and ask them to check that the feature is properly configured.")
        msg = msg.replace('@everyone', '@\u200beveryone').replace('@here', '@\u200bhere')
        message_id = await self.send_anon_webhook(chan, "Anon", msg)
        AnonDB.set_message(message_id, ctx.author.id, guild_id)
        await ctx.message.add_reaction('✅')

    @staticmethod
    async def send_anon_webhook(channel: discord.TextChannel, author: str, content: str):
        webhooks = await channel.webhooks()
        webhook = webhooks[0]
        msg = await webhook.send(content=content, username=author, wait=True)
        return msg.id

    
    @commands.group()
    async def private(self, ctx):
        return

    @private.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx, role: discord.Role, name: str = "Private Category", name_prefix: str = "private"):
        private = {}
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),

            role: discord.PermissionOverwrite(read_messages=True)
        }
        msg = await ctx.send("Creating private category...")
        cat: discord.CategoryChannel = await ctx.guild.create_category(name=name, overwrites=overwrites,
                                                                       reason="Private channels setup")
        hub = await cat.create_text_channel(name="private-hub", overwrites=overwrites, reason="Private channels setup")
        private["cat_id"] = cat.id
        private["guild_id"] = ctx.guild.id
        private["role_id"] = role.id
        private["name_prefix"] = name_prefix
        private["hub_id"] = hub.id

        PrivateDB.create_one(private)

        await msg.edit(content="Private category is ready !")
        msg = await hub.send(
            "Hey ! This is the hub channel. Use `--private create` to start with your own private channel !")
        await msg.pin()

    @private.command()
    @commands.guild_only()
    async def create(self, ctx):
        cat: discord.CategoryChannel = ctx.message.channel.category
        privates = PrivateDB.get_one(ctx.guild.id, cat.id)
        if not privates:
            return
        if ctx.channel.id != privates["hub_id"]:
            return
        has_channel = PrivateDB.has_channel(ctx.author.id, cat.id)
        if has_channel:
            await ctx.send("You already have a private channel ! You can't get more than one channel...")
            return

        msg = await ctx.send("Creating private channel...")
        role = ctx.guild.get_role(privates["role_id"])
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            ctx.author: discord.PermissionOverwrite(read_messages=True),
            role: discord.PermissionOverwrite(read_messages=True)
        }
        chan = await cat.create_text_channel(name="{}-{}".format(privates["name_prefix"], ctx.author.name),
                                             overwrites=overwrites,
                                             reason="Creating private channel for {}".format(ctx.author.name))
        PrivateDB.create_user_one(ctx.author.id, cat.id, chan.id)
        await msg.edit(content="The private channel has been created !")
        await chan.send("Your private channel is ready. If you want to delete it, run : `--private leave`.\n{}".format(
            ctx.author.mention))

    @private.command()
    @commands.guild_only()
    async def leave(self, ctx):
        cat: discord.CategoryChannel = ctx.message.channel.category
        users = PrivateDB.get_user(ctx.author.id, cat.id)
        if not ctx.channel.id == users["chan_id"]:
            return
        else:
            await ctx.channel.delete()
            PrivateDB.delete_user(ctx.author.id, cat.id)

    @staticmethod
    async def send_webhook(channel: discord.TextChannel, author: discord.Member, content: list):
        webhooks = await channel.webhooks()
        webhook = webhooks[0]
        await webhook.send(embeds=content, username=author.name, avatar_url=author.avatar_url)
"""


def setup(bot):
    bot.add_cog(Custom(bot))
