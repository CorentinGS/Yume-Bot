import json
import os
import random
from datetime import datetime

import discord
from discord.ext import commands

from modules.utils.db import Settings


class Sanction():

    async def create_sanction(self, ctx, user, event, mod, guild, reason=None, time=None):
        a = datetime.now()
        _id = int(a.strftime('%Y%m%d%H%M%S%f'))

        set = await Settings().get_sanction_settings(str(_id))

        set['user'] = user.name
        set['user_id'] = str(user.id)
        set['event'] = event
        set['moderator'] = mod.name
        set['moderator_id'] = str(mod.id)
        set['guild'] = guild.name
        set['guild_id'] = str(guild.id)
        set['reason'] = reason
        set['time'] = str(time)
        set['date'] = str(a)

        await Settings().set_sanction_settings(str(_id), set)

        return _id

    async def create_strike(self, user, event, guild, reason=None):
        a = datetime.now()
        _id = int(a.strftime('%Y%m%d%H%M%S%f'))

        set = await Settings().get_sanction_settings(str(_id))

        set['user'] = user.name
        set['user_id'] = str(user.id)
        set['event'] = event
        set['moderator'] = "Automod"
        set['moderator_id'] = str(456504213262827524)
        set['guild'] = guild.name
        set['guild_id'] = str(guild.id)
        set['reason'] = reason
        set['time'] = None
        set['date'] = str(a)

        await Settings().set_sanction_settings(str(_id), set)

        return _id

    async def find_sanction(self, ctx, id):
        set = await Settings().get_sanction_settings(str(id))
        event = set["event"]
        em = discord.Embed()
        em.set_author(name="Sanction report",
                      icon_url=ctx.message.author.avatar_url)

        if "event" not in set:

            em.description = f"Sanction not found"

        else:

            em.set_footer(text=f"ID : {id}")
            em.description = f"Type: {event}"
            em.add_field(name="User", value=set['user'])
            em.add_field(name="User Id", value=set['user_id'])
            em.add_field(name="Moderator", value=set['moderator'])
            em.add_field(name="Moderator_id", value=set['moderator_id'])

            if set['reason'] is not None:
                em.add_field(name="Reason", value=set['reason'])
            if set['time'] is not None:
                em.add_field(name="Time", value=set['time'])
            em.add_field(name="Date", value=set['date'])

        return em
