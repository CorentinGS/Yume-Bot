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
import discord
from discord.ext import commands

from modules.sql.privatedb import PrivateDB


class Custom(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

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
        await hub.send("Hey ! This is the hub channel. Use `--private create` to start with your own private channel !")

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


def setup(bot):
    bot.add_cog(Custom(bot))
