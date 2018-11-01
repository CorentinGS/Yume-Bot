import discord
from discord.ext import commands
import datetime
import asyncio


class Embeds():

    async def format_mod_embed(self, ctx, user, success, command, duration=None):
        em = discord.Embed(timestamp=ctx.message.created_at)
        em.set_author(name=command.title(), icon_url=user.avatar_url)
        em.set_footer(text=f'User ID: {user.id}')
        if success:
            if command == 'ban'or command == 'hackban':
                em.description = f'**{user}** was just {command}ned...'
            elif command == 'mute':
                em.description = f'**{user}** was just muteded for {duration}...'
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
