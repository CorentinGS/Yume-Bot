from datetime import datetime

import dateutil.relativedelta
import discord

from modules.utils.db import Settings


class Sanction:

    @staticmethod
    async def create_sanction(user, event, mod, guild, reason=None, time=None):
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

    @staticmethod
    async def create_strike(user, event, guild, reason=None):
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

    @staticmethod
    async def find_sanction_id(ctx, id):
        set = await Settings().get_sanction_settings(str(id))
        event = set["event"]
        em = discord.Embed()
        em.set_author(name="Sanction report")

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

    @staticmethod
    async def find_sanction_member(ctx, member: discord.Member, guild: discord.Guild):
        strike = await Settings().get_sanction_settings_user(str(member.id), str(guild.id))
        em = discord.Embed()
        em.set_author(name=f"Sanction report | {member.name}",
                      icon_url=member.avatar_url)

        today = datetime.now()

        msg = "__Sanction__\n\n"

        for sanction in strike:
            sanc = await Settings().get_sanction_settings(sanction)
            date = datetime.strptime(sanc['date'], '%Y-%m-%d %H:%M:%S.%f')

            rd = dateutil.relativedelta.relativedelta(date, today)
            str1 = "**" + sanc['event'] + " |** " + (str(abs(rd.years)) + " years " if rd.years != 0 else "") \
                   + (str(abs(rd.months)) + " months " if rd.months != 0 else "") \
                   + (str(abs(rd.days)) + " days " if rd.days != 0 else "") \
                   + (str(abs(rd.hours)) + " hours " if rd.hours != 0 else "") \
                   + (str(abs(rd.minutes)) + " minutes " if rd.minutes != 0 else "") + "ago\n"
            msg = " ".join((msg, str1))

        em.description = msg

        return em
