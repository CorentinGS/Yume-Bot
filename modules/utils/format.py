import discord
from discord.ext import commands
import datetime
import asyncio
import random

from modules.utils.db import Settings

from modules.utils import lists


class Embeds():

    async def format_mod_embed(self, ctx, user, command, duration=None):
        tip = random.choice(lists.tip)

        em = discord.Embed(timestamp=ctx.message.created_at)
        em.set_author(name=f"{command}", icon_url=user.avatar_url)
        em.set_footer(text=f'Tip: {tip}')
        if command == 'ban' or command == 'hackban':
            em.description = f'**{user}** was just {command}ned...'
        elif command == 'mute':
            em.description = f'**{user}** was just muted for {duration}...'
        elif command == 'unmute':
            em.description = f'**{user}** was just unmuted...'
        elif command == 'kick':
            em.description = f'**{user}** was just kicked...'
        elif command == 'unban':
            em.description = f'**{user}** was just unbanned...'
        else:
            return

        return em

    async def format_feedback_embed(self, ctx, auth, guild, success, message):
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
     # TODO: Add Auto invite link !
            em.set_footer(text=tip)
        else:
            pass
        return em

    async def format_set_embed(self, ctx, guild, command, vip):
        tip = random.choice(lists.tip)

        em = discord.Embed(timestamp=ctx.message.created_at)
        em.set_author(name='Settings', icon_url=guild.icon_url)
        em.set_footer(text=f'Tip: {tip}')
        if command == 'setting':
            em.add_field(name="🇬 **Greet**", value="Greet Menu")
            em.add_field(name="⛔ **Blacklist**", value='Blacklist Menu')
            em.add_field(name="🖊 **Logging**", value="Logging Menu")
            em.add_field(name="🔨 **Automoderation**", value="AutoMod Menu")
            em.add_field(name="❌", value="Leave")

        elif command == 'greetmenu':
            em.add_field(name="❔ **Channel**", value="Set the greet channel")
            em.add_field(name="📜 **Toggle**", value="Toggle Greet")
            em.add_field(name="❌", value="Leave")

        elif command == 'blacklistmenu':
            em.add_field(name="🚫 **Activate**",
                         value="Activate the Global blacklist", inline=False)
            em.add_field(name="🔓 **Desactivate**",
                         value="Desactivate the Global blacklist")
            em.add_field(name="❌", value="Leave")

        elif command == 'loggingmenu':
            em.add_field(name="📋 **Activate**",
                         value="Activate Logging", inline=False)
            em.add_field(name="🆓 **Desactivate**",
                         value="Desactivate Logging", inline=False)
            em.add_field(name="❔ **Channel**", value="Set the logging channel")
            '''
            if vip is True:
                em.add_field(name="🎬 **Vip Logging**", value = 'Full logging', inline = False)
            '''
            em.add_field(name="❌", value="Leave")

        elif command == 'automenu':
            em.add_field(name='✅ **Activate**',
                         value='Activate AutoModeration', inline=False)
            em.add_field(name='🚫 **Desactivate**',
                         value='Desactivate AutoModeration', inline=False)
            em.add_field(
                name='!!!!!', value='This module is still experimental, Please report all issues using --feedback')

            if vip is True:
                em.add_field(name='⛔ **AntiRaid**',
                             value='Toggle Antiraid', inline=False)

            em.add_field(name="❌", value="Leave")

        return em

    async def format_get_set_embed(self, ctx, guild, greet, greetchannel, blacklist, logging, logchannel, automod):
        tip = random.choice(lists.tip)

        em = discord.Embed(timestamp=ctx.message.created_at)
        em.set_author(name='Settings')
        em.set_footer(text=f'Tip: {tip}')

        em.add_field(name="Greet", value=greet)
        em.add_field(name="Greet Channel", value=greetchannel)
        em.add_field(name="Blacklist", value=blacklist)
        em.add_field(name="Logging", value=logging)
        em.add_field(name="Log Channel", value=logchannel)
        em.add_field(name='Automod', value=automod)

        return em

    async def format_profile_embed(self, ctx, user, command, vip):
        tip = random.choice(lists.tip)

        em = discord.Embed(timestamp=ctx.message.created_at)
        em.set_author(name='Profile', icon_url=user.avatar_url)
        em.set_footer(text=f'Tip: {tip}')
        if command == "edit":
            em.add_field(name="❓ **Gender**", value="Select a gender")
            em.add_field(name="❤ **Love**", value="Are u in love ?")
            em.add_field(name="🖊 **Description**", value='Who are you ?')
            em.add_field(name="❌", value="Leave", inline=False)

        elif command == 'gender':
            em.add_field(name="👦", value="Male")
            em.add_field(name="👩", value="Female")
            em.add_field(name="💥", value="Transgender")
            em.add_field(name='🐌', value="Non-Binary")

            if vip is True:
                em.add_field(name='🐧', value='Penguin')
                em.add_field(name='🐱', value="Cat")
            em.add_field(name="❌", value="Leave", inline=False)

        return em

    async def format_desc_profile_embed(self, ctx, user, content):
        tip = random.choice(lists.tip)

        em = discord.Embed(timestamp=ctx.message.created_at)
        em.set_author(name='Profile', icon_url=user.avatar_url)
        em.set_footer(text=f'Tip: {tip}')

        em.add_field(name='🖊', value='Edit')
        em.add_field(name="❌", value="Leave", inline=False)

        em.description = '{}'.format(str(content))

        return em

    async def format_get_profile_embed(self, ctx, user, vip, gender, status, lover, desc, xp, reach, level):
        tip = random.choice(lists.tip)

        em = discord.Embed(timestamp=ctx.message.created_at)
        em.set_author(name='Profile', icon_url=user.avatar_url)
        em.set_footer(text=f'Tip: {tip}')
        em.description = desc

        if gender == "male":
            emote = "👦"
        elif gender == 'female':
            emote = '👩'
        elif gender == "transgender":
            emote = "💥"
        elif gender == 'non-binary':
            emote = "🐌"
        elif gender == "penguin":
            emote = '🐧'
        elif gender == "cat":
            emote = '🐱'
        else:
            emote = '❓'
            gender = 'Unknown'

        em.add_field(name="**Gender**",
                     value=f"{emote} {gender}", inline=False)
        em.add_field(name="**Vip**", value=vip, inline=False)

        if status == 'alone':
            em.add_field(name='**Status**', value='💔 Alone...', inline=False)
        else:
            em.add_field(name='**Status**',
                         value=f'❤ **{lover}**', inline=False)

        em.add_field(name="**Level**", value=f"{level}")
        em.add_field(name='**Xp**', value=f"{xp}/{reach}")

        return em

        # TODO: Simplifier le système d'emote

    async def format_love_embed(self, ctx, auth, command):
        tip = random.choice(lists.tip)

        em = discord.Embed(timestamp=ctx.message.created_at)
        em.set_author(name='Love', icon_url=auth.avatar_url)
        em.set_footer(text=f'Tip: {tip}')

        if command == "love":
            em.add_field(name="💘", value="Love declaration")

        elif command == 'declaration':
            em.description = "{} is in love with you and wants to be in a relationship with you, do you accept? ".format(
                auth)

        return em
