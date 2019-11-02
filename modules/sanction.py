import typing
from datetime import datetime

import dateutil.relativedelta
import discord

from modules.utils.db import Settings
from modules.utils.sanctiony import SanctionY


class Sanction:

    @staticmethod
    async def create_sanction(user, event, mod, guild, reason=None, time=None):
        id = int(datetime.now().strftime('%Y%m%d%H%M%S%f'))

        sanction = SanctionY(str(id))

        sanction.user = user.name
        sanction.user_id = str(user.id)
        sanction.event = event
        sanction.mod = mod.name
        sanction.mod_id = str(mod.id)
        sanction.guild = guild.name
        sanction.guild_id = str(guild.id)
        sanction.reason = reason
        sanction.time = str(time)

        await sanction.set()
        return sanction.id


    @staticmethod
    async def create_strike(user, event, guild, reason=None):
        id = int(datetime.now().strftime('%Y%m%d%H%M%S%f'))
        sanction = SanctionY(str(id))

        sanction.user = user.name
        sanction.user_id = str(user.id)
        sanction.event = event
        sanction.mod = "Automod"
        sanction.mod_id = str(456504213262827524)
        sanction.guild = guild.name
        sanction.guild_id = str(guild.id)
        sanction.reason = reason
        sanction.time = None

        await sanction.set()
        return sanction.id


    @staticmethod
    async def find_sanction_id(ctx, id):
        sanction = SanctionY(str(id))
        toto = await sanction.get()
        em = discord.Embed()
        em.set_author(name="Sanction report")

        if toto is False:
            em.description = f"Sanction not found"
        else:
            em.set_footer(text=f"ID : {id}")
            em.description = f"Type: {sanction.event}"
            em.add_field(name="User", value=sanction.user)
            em.add_field(name="User Id", value=sanction.user_id)
            em.add_field(name="Moderator", value=sanction.mod)
            em.add_field(name="Moderator_id", value=sanction.mod_id)


            em.add_field(name="Reason", value=sanction.reason)
            em.add_field(name="Time", value=sanction.time)
            em.add_field(name="Date", value=sanction.date)
        return em


    @staticmethod
    async def find_sanction_member(ctx, member: typing.Union[discord.Member, discord.User], guild: discord.Guild):
        strikes = await Settings().get_sanction_settings_member(str(member.id), str(guild.id))
        em = discord.Embed()
        em.set_author(name=f"Sanction report | {member.name}",
                      icon_url=member.avatar_url)

        today = datetime.now()

        msg = "__Sanction__\n\n"

        for sanction in strikes:
            sanc = await Settings().get_sanction_settings(sanction)
            date = datetime.strptime(str(sanc['date']), '%Y-%m-%d %H:%M:%S.%f')

            rd = dateutil.relativedelta.relativedelta(date, today)
            str1 = "**" + sanc['event'] + " |** " + (str(abs(rd.years)) + " years " if rd.years != 0 else "") \
                   + (str(abs(rd.months)) + " months " if rd.months != 0 else "") \
                   + (str(abs(rd.days)) + " days " if rd.days != 0 else "") \
                   + (str(abs(rd.hours)) + " hours " if rd.hours != 0 and rd.months == 0 else "") \
                   + (str(abs(rd.minutes)) + " minutes " if rd.minutes != 0 and rd.days == 0 else "") \
                   + (str(abs(rd.seconds)) + " seconds " if rd.minutes == 0 else "") + "ago\n"
            msg = " ".join((msg, str1))

        em.description = msg

        return em
