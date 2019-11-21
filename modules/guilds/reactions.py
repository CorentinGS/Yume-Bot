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

#
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#
import typing

import discord
from discord.ext import commands

from modules.utils.db import Settings


class ReactionY:
    def __init__(self, guild: discord.Guild, channel: discord.TextChannel, message: discord.Message):
        # Settings
        self.channel: int = channel.id
        self.guild: int = guild.id
        self.message: int = message.id
        self.reaction: str = ''
        self.role: int = 0

    async def set(self):
        set = await Settings().get_reaction_settings(str(self.guild))

        # Store
        if not str(self.channel) in set:
            d = {
                str(self.message): {
                    str(self.reaction): self.role
                }
            }
            set[str(self.channel)] = d
        elif not str(self.message) in set[str(self.channel)]:
            set[str(self.channel)][str(self.message)] = {
                str(self.reaction): self.role
            }

        else:
            set[str(self.channel)][str(self.message)][str(self.reaction)] = self.role

        await Settings().set_reaction_settings(str(self.guild), set)

    async def get(self, reaction):
        set = await Settings().get_reaction_settings(str(self.guild))

        # Settings
        self.reaction = reaction
        if not str(self.channel) in set:
            return
        elif not str(self.message) in set[str(self.channel)]:
            return
        elif not str(self.reaction) in set[str(self.channel)][str(self.message)]:
            return
        else:
            self.role = set[str(self.channel)][str(self.message)][str(self.reaction)]
            return True


class Reactions(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.command()
    @commands.guild_only()
    async def arr(self, ctx, channel: typing.Union[discord.TextChannel, int], message_id: int,
                  role: typing.Union[str, discord.Role],
                  emoji: typing.Union[str, discord.Emoji]):

        if not isinstance(channel, discord.TextChannel):
            try:
                role = discord.utils.get(ctx.guild.text_channels, id=channel)
            except discord.NotFound:
                return await ctx.send(
                    "We can't find the channel")
            except discord.InvalidArgument:
                return await ctx.send("We can't find the channel.")

        if not isinstance(role, discord.Role):
            try:
                role = discord.utils.get(ctx.guild.roles, name=role)
            except discord.NotFound:
                return await ctx.send(
                    "We can't find the role")
            except discord.InvalidArgument:
                return await ctx.send("We can't find the role.")

        try:
            message = await channel.fetch_message(message_id)
        except discord.NotFound:
            return await ctx.send(
                "We can't find the message")
        except discord.HTTPException:
            return await ctx.send("We can't find the message.")

        try:
            await message.add_reaction(emoji)
        except discord.InvalidArgument:
            return await ctx.send("The emoji isn't valid.")
        except discord.NotFound:
            return await ctx.send("The emoji isn't valid.")

        reac = ReactionY(ctx.guild, channel, message)
        reac.reaction = emoji
        reac.role = role.id
        await reac.set()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        channel = self.bot.get_channel(payload.channel_id)
        author = channel.guild.get_member(payload.user_id)
        if author.bot:
            return
        message = await channel.fetch_message(payload.message_id)

        reac = ReactionY(channel.guild, channel, message)

        emoji = payload.emoji

        if await reac.get(emoji):
            try:
                role = discord.utils.get(channel.guild.roles, id=reac.role)
            except discord.NotFound:
                return
            await author.add_roles(role, reason="Role Reaction")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):

        channel = self.bot.get_channel(payload.channel_id)
        author = channel.guild.get_member(payload.user_id)
        if author.bot:
            return
        message = await channel.fetch_message(payload.message_id)

        reac = ReactionY(channel.guild, channel, message)

        emoji = payload.emoji

        if await reac.get(emoji):
            try:
                role = discord.utils.get(channel.guild.roles, id=reac.role)
            except discord.NotFound:
                return
            await author.remove_roles(role, reason="Role Reaction")


def setup(bot):
    bot.add_cog(Reactions(bot))
