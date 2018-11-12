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
            em.add_field(name= "❌", value= "Leave")


        elif command == 'greetmenu':
            em.add_field(name= "❔ **Channel**", value= "Set the greet channel")
            em.add_field(name="📜 **Toggle**", value= "Toggle Greet")
            em.add_field(name= "❌", value= "Leave")



        return em
