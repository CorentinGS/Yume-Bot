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

import discord
from discord.ext import commands

from modules.sql.guilddb import GuildDB
from modules.utils import lists


class Event(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """

        :param member: The member who joined the guild
        """

        guild = GuildDB.get_one(member.guild.id)

        if guild.greet:
            channel = self.bot.get_channel(int(guild.greet_chan))
            greet = random.choice(lists.greet)

            em = discord.Embed(timestamp=member.joined_at)
            em.set_author(name="Welcome", icon_url=member.avatar_url)
            em.set_footer(text=f'{member.name}')
            em.description = f"{greet}"
            await channel.send(embed=em)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """

        :param member: The member who has left
        """

        guild = GuildDB.get_one(member.guild.id)

        if guild.greet:
            try:
                channel = member.guild.get_channel(int(guild.greet_chan))
            except discord.HTTPException:
                pass
            else:
                greet = random.choice(lists.leave)

                em = discord.Embed(timestamp=member.joined_at)
                em.set_author(name="Bye", icon_url=member.avatar_url)
                em.set_footer(text=f'{member.name}')
                em.description = f"{greet}"
                await channel.send(embed=em)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not isinstance(message.channel, discord.DMChannel) or message.clean_content.startswith(
                "--") or message.author.bot:
            return
        try:
            guild: discord.Guild = self.bot.get_guild(488765635439099914)
        except discord.HTTPException:
            return
        chan: discord.TextChannel = guild.get_channel(743198460055912478)
        user: discord.User = message.channel.recipient
        webhooks = await chan.webhooks()
        webhook = webhooks[0]

        await webhook.send(content=message.clean_content, username=user.name, avatar_url=user.avatar_url, wait=True)


def setup(bot):
    bot.add_cog(Event(bot))
