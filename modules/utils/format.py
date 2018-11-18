import discord
from discord.ext import commands
import datetime
import asyncio

from modules.utils.db import Settings


class Embeds():

    async def format_mod_embed(self, ctx, user, success, command, duration=None):
        em = discord.Embed(timestamp=ctx.message.created_at)
        em.set_author(name=command.title(), icon_url=user.avatar_url)
        em.set_footer(text=f'User ID: {user.id}')
        if success:
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
                pass
        else:
            return

        return em

    async def format_feedback_embed(self, ctx, auth, guild, success, message):
        em = discord.Embed(timestamp= ctx.message.created_at)
        em.set_author(name="Feedback", icon_url=auth.avatar_url)
        if success:
            em.add_field(name = "Author", value=f"Name : {auth} \n ID : {auth.id}", inline = False)
            em.add_field(name = "Guild", value=f"Name : {guild.name} \n ID : {guild.id}", inline = False)
            em.add_field(name = "Content", value = f"{message.content}", inline= False)
     # TODO: Add Auto invite link !
            em.set_footer(text=message)
        else:
            pass
        return em

    async def format_set_embed(self, ctx, guild, command):
        em = discord.Embed(timestamp= ctx.message.created_at)
        em.set_author(name='Settings', icon_url=guild.icon_url)
        if command == 'setting':
            em.add_field(name= "🇲 **Mute**", value= "Settings for Mute")
            em.add_field(name= "🇬 **Greet**", value= "Settings for Greet")
            em.add_field(name= "❌", value= "Leave")

        elif command == 'mutemenu':
            em.add_field(name= "💂 **Role**", value= "Toggle Role Mute")
            em.add_field(name= "💣 **Permissions**", value= "Toggle Permissions Mute")
            em.add_field(name= "❌", value= "Leave", inline=False)


        elif command == 'greetmenu':
            em.add_field(name= "❔ **Channel**", value= "Set the greet channel")
            em.add_field(name="📜 **Toggle**", value= "Toggle Greet")
            em.add_field(name= "❌", value= "Leave")

        return em

    async def format_profile_embed(self, ctx, user, command, vip):
        em = discord.Embed(timestamp= ctx.message.created_at)
        em.set_author(name='Profile', icon_url=user.avatar_url)
        if command == "edit":
            em.add_field(name= "❓ **Gender**", value= "Select a gender" )
            em.add_field(name= "❤ **Love**", value= "Are u in love ?" )
            em.add_field(name= "❌", value= "Leave", inline=False)

        elif command == 'gender':
            em.add_field(name= "👦", value= "Male")
            em.add_field(name= "👩", value= "Female")
            em.add_field(name= "💥", value= "Transgender")
            em.add_field(name= '🐌', value= "Non-Binary")

            if vip is True:
                em.add_field(name= '🐧', value= 'Penguin')
                em.add_field(name= '🐱', value= "Cat")
            em.add_field(name= "❌", value= "Leave", inline=False)


        return em

    async def format_get_profile_embed(self, ctx, user, vip, gender, status, lover):
        em = discord.Embed(timestamp = ctx.message.created_at)
        em.set_author(name= 'Profile', icon_url = user.avatar_url)

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

        em.add_field(name = emote, value = gender)
        em.add_field(name = "Vip", value= vip)

        if status == 'alone':
            em.add_field(name = '💔', value = 'Alone...', inline = False)
        else:
            em.add_field(name ='❤', value = lover, inline = False)

        return em

        # TODO: Simplifier le système d'emote


    async def format_love_embed(self, ctx, auth, command):
        em = discord.Embed(timestamp = ctx.message.created_at)
        em.set_author(name= 'Love', icon_url = auth.avatar_url)

        if command == "love":
            em.add_field(name= "💘", value= "Love declaration")

        elif command == 'declaration':
            em.description = "{} is in love with you and wants to be in a relationship with you, do you accept? ".format(auth)
            em.add_field(name ='✅', value = "Yes")
            em.add_field(name = '❌', value = 'No')

        return em

            # TODO: Un menu pour "LOVE"
