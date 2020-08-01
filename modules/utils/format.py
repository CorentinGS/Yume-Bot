#  Copyright (c) 2020.
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

import dateutil
import discord

from modules.sql.sanctions import Sanction
from modules.sql.sanctionsdb import SanctionsDB
from modules.utils import lists


class Mod:

    @staticmethod
    async def check_embed(member, guild, sanctions, time):
        em = discord.Embed(
            title="{}".format(member.name),
            description="A new user has joined",
            color=discord.Colour.magenta()
        )
        em.set_author(name=f"{guild.name}")
        em.set_thumbnail(url=member.avatar_url)
        em.add_field(name="User", value=f"Name : {member.mention} \nID : {member.id}")
        em.add_field(name="Informations", value=f"Sanctions : {sanctions} \nAge : {time}days")

        return em


class Embeds:

    @staticmethod
    async def format_automod_embed(user, reason, sanction_id, message):
        em = discord.Embed(color=discord.Colour.gold(), timestamp=message.created_at)
        em.set_author(name="Automod")
        em.set_footer(text=f'Sanction ID: {sanction_id}')
        msg = f"**Guilty** : {user.name}#{user.discriminator}<{user.id}>\n" \
              f"**Reason** : {reason}\n"
        em.description = msg
        return em

    @staticmethod
    async def format_social_embed(text, act: str, url, message):
        em = discord.Embed(color=discord.Colour.gold(), timestamp=message.created_at)
        em.set_author(name=f"{text}")
        em.set_footer(text=f'{act}')
        em.set_image(url=url)
        return em

    @staticmethod
    async def format_mod_embed(ctx, user, mod, reason, command, sanction=None, duration=None):

        if command == "ban" or command == "hackban":
            color = discord.Colour.red()
        if command == "unban" or "unmute":
            color = discord.Colour.green()
        if command == "kick":
            color = discord.Colour.blue()
        if command == "mute":
            color = discord.Colour.orange()
        if command == "strike":
            color = discord.Colour.gold()

        em = discord.Embed(color=color, timestamp=ctx.message.created_at)
        em.set_author(name=f"{command.title()}")
        if sanction is not None:
            em.set_footer(text=f'Sanction ID: {sanction}')

        if isinstance(mod, (discord.Member, discord.User)):
            msg = f"**Guilty** : {user.name}#{user.discriminator}<{user.id}>\n" \
                  f"**Moderator** : {mod.name}#{mod.discriminator}\n"
        else:
            msg = f"**Guilty** : {user.name}#{user.discriminator}<{user.id}>\n" \
                  f"**Moderator** : Auto\n"
        if reason is not None:
            str1 = f"**Reason** : {reason}\n"
            msg = " ".join((msg, str1))
        if duration is not None:
            str2 = f"**Duration**: {duration}"
            msg = " ".join((msg, str2))
        em.description = msg

        return em

    @staticmethod
    async def format_feedback_embed(ctx, auth, guild, success, message):
        tip = random.choice(lists.tip)

        em = discord.Embed(timestamp=ctx.message.created_at)
        em.set_author(name="Feedback", icon_url=auth.avatar_url)
        if success:
            em.add_field(
                name="Author", value=f"Name : {auth} \n ID : {auth.id}", inline=False)
            em.add_field(
                name="Guild", value=f"Name : {guild.name} \n ID : {guild.id}", inline=False)
            em.add_field(name="Content",
                         value=f"{message.content}", inline=False)
            em.set_footer(text=tip)

        return em

    @staticmethod
    async def format_get_set_embed(ctx, greet, greetchannel, blacklist, logging, logchannel, vip, color,
                                   stats_channels):
        tip = random.choice(lists.tip)
        em = discord.Embed(timestamp=ctx.message.created_at)
        em.set_author(name='Settings')
        em.set_footer(text=f'Tip: {tip}')

        em.add_field(name="Greet", value=greet)

        greetchan = discord.utils.get(ctx.guild.text_channels, id=int(greetchannel))
        if not isinstance(greetchan, discord.TextChannel):
            em.add_field(name="Greet Channel", value="None")
        else:
            em.add_field(name="Greet Channel", value=greetchan.mention)

        em.add_field(name="Logging", value=logging)

        logchan = discord.utils.get(ctx.guild.text_channels, id=int(logchannel))
        if not isinstance(logchan, discord.TextChannel):
            em.add_field(name="Log Channel", value="None")
        else:
            em.add_field(name="Log Channel", value=logchan.mention)

        em.add_field(name="Blacklist", value=blacklist)
        em.add_field(name='Vip', value=vip)
        em.add_field(name='Color', value=color)
        em.add_field(name='Stats Channel', value=stats_channels)

        return em

    @staticmethod
    async def format_commands_embed(ctx, icon):
        em = discord.Embed(timestamp=ctx.message.created_at)
        em.set_author(name='Yume Bot', url="https://www.yumenetwork.net/documentation/", icon_url=icon)
        em.description = "**» Does anyone need any help?**\n" \
                         "You can use **--h <category>** to view commands for that category."
        em.add_field(name="**Categories**", value="**--h general** | General Commands\n"
                                                  "**--h fun** | Fun Commands\n"
                                                  "**--h utils** | Utils Commands\n"
                                                  "**--h mods** | Mods Commands\n"
                                                  "**--h admin** | Admin Commands\n"
                                                  "**--h level** | Level Commands\n"
                                                  "**--h guild** | Guild Commands\n"
                                                  "**--h info** | Information Commands\n"
                                                  "**--h social** | Social Commands\n"
                                                  "**--h game** | Game Commands\n"
                                                  "**--h nsfw** | Nsfw Commands"
                     )

        em.add_field(name="Links", value="[Support]("
                                         "https://www.yumenetwork.net/invite/) | [Sources]("
                                         "https://github.com/yumenetwork/Yume-Bot) | "
                                         "[Invite]"
                                         "(https://www.yumenetwork.net/botinvite/) | "
                                         "[Site](https://www.yumenetwork.net)",
                     inline=False)

        return em

    @staticmethod
    async def format_cat_embed(ctx, icon, category, liste):
        em = discord.Embed(timestamp=ctx.message.created_at)
        em.set_author(name='Yume Bot', url="https://yumenetwork.gitbook.io/yumebot/", icon_url=icon)
        em.description = f"**Category : {category}**" \
                         f"\nYou can get more info about a command [here]" \
                         f"(https://yumenetwork.gitbook.io/yumebot/commands/{str.lower(category)})"
        em.add_field(name="**:pushpin: Commands**", value=f"{liste}")

        return em

    @staticmethod
    async def format_sanction_embed(bot, sanction: Sanction):
        user = await bot.fetch_user(sanction.user_id)
        mod = await bot.fetch_user(sanction.moderator_id)
        em = discord.Embed()
        em.set_author(name="Sanction report")

        em.set_footer(text=f"ID : {sanction.sanction_id}")
        em.description = f"Type: {sanction.event}"
        em.add_field(name="User", value=user.name)
        em.add_field(name="User Id", value=sanction.user_id)
        em.add_field(name="Moderator", value=mod.name)
        em.add_field(name="Moderator_id", value=sanction.moderator_id)

        em.add_field(name="Reason", value=sanction.reason)
        em.add_field(name="Time", value=sanction.time)
        em.add_field(name="Date", value=sanction.event_date)
        return em

    @staticmethod
    async def user_list_sanction_embed(sanctions, member):

        em = discord.Embed()
        em.set_author(name=f"Sanction report | {member.name}",
                      icon_url=member.avatar_url)

        today = datetime.now()

        msg = "__Sanctions__\n\n"

        for sanction in sanctions:
            sanction = SanctionsDB.get_sanction(sanction)

            date = sanction.event_date

            str1 = "**" + sanction.event + " |** " + str(date) + "\n"
            msg = " ".join((msg, str1))

        em.description = msg

        return em

    @staticmethod
    async def command_help(ctx, bot: discord.User, command: str, description: str, usage: str, examples: str = None,
                           permission: str = None):
        em = discord.Embed(timestamp=ctx.message.created_at)
        em.set_author(name='Yume Bot', url="https://yumenetwork.net", icon_url=bot.avatar_url)
        em.title = f"{command}"
        em.description = f"{description}\n\nUsage:\n`{usage}`"
        if examples:
            em.add_field(name="Examples", value=examples, inline=True)
        if permission:
            em.add_field(name="Permission", value=f"{permission}")
        return em
