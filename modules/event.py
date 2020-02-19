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

        if guild.stats_channels:
            category = discord.utils.get(
                member.guild.categories, id=int(guild.stats_category))
            for channel in category.channels:
                try:
                    await channel.delete()
                except discord.Forbidden:
                    return
                except discord.HTTPException:
                    return

            overwrite = {
                member.guild.default_role: discord.PermissionOverwrite(connect=False),
            }

            await member.guild.create_voice_channel(f'Users : {len(member.guild.members)}', overwrites=overwrite,
                                                    category=category)
            bots = []
            for user in member.guild.members:
                if user.bot is True:
                    bots.append(user)
            await member.guild.create_voice_channel(f'Bots : {len(bots)}', overwrites=overwrite, category=category)
            await member.guild.create_voice_channel(f'Members : {len(member.guild.members) - len(bots)}',
                                                    overwrites=overwrite, category=category)

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

        if guild.stats_channels:
            try:
                category = discord.utils.get(
                    member.guild.categories, id=int(guild.stats_category))
            except discord.HTTPException:
                return
            else:
                for channel in category.channels:
                    try:
                        await channel.delete()
                    except discord.Forbidden:
                        return
                    except discord.HTTPException:
                        return

                overwrite = {
                    member.guild.default_role: discord.PermissionOverwrite(connect=False),
                }

                await member.guild.create_voice_channel(f'Users : {len(member.guild.members)}', overwrites=overwrite,
                                                        category=category)
                bots = []
                for user in member.guild.members:
                    if user.bot is True:
                        bots.append(user)
                await member.guild.create_voice_channel(f'Bots : {len(bots)}', overwrites=overwrite, category=category)
                await member.guild.create_voice_channel(f'Members : {len(member.guild.members) - len(bots)}',
                                                        overwrites=overwrite, category=category)


def setup(bot):
    bot.add_cog(Event(bot))
