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

import typing
from datetime import datetime

import discord
from sqlalchemy import and_

from modules.sql.dbConnect import Db
from model.sanctions import Sanction


class SanctionsDB:

    @staticmethod
    def sanction_from_row(rows) -> Sanction:
        return Sanction(rows[0], rows[1], rows[2], rows[3], rows[4],
                        rows[5], rows[6], rows[7])

    """
    Get methods
    """

    @staticmethod
    def get_sanction(sanction_id: int) -> Sanction:
        con, meta = Db.connect()
        t_sanction = meta.tables['sanctions']
        try:
            clause = t_sanction.select().where(t_sanction.c.sanction_id == str(sanction_id))
            rows = con.execute(clause)
            row = rows.fetchone()
            if row:
                return SanctionsDB.sanction_from_row(row)
        except Exception as err:
            print(err)

    @staticmethod
    def get_sanctions_from_guild_user(guild: discord.Guild, user: discord.Member) -> list:
        con, meta = Db.connect()
        t_sanction = meta.tables['sanctions']
        sanctions = []

        try:
            clause = t_sanction.select().where(
                and_(t_sanction.c.user_id == str(user.id),
                     t_sanction.c.guild_id == str(guild.id)))
            for row in con.execute(clause):
                sanctions.append(SanctionsDB.sanction_from_row(row))
            return sanctions
        except Exception as err:
            print(err)

        return []

    """
    Create & delete methods
    """

    @staticmethod
    def create_sanction(sanction: Sanction):
        con, meta = Db.connect()
        t_sanction = meta.tables['sanctions']
        try:
            clause = t_sanction.insert().values(
                event=sanction.event,
                event_date=sanction.event_date,
                guild_id=sanction.guild_id,
                moderator_id=sanction.moderator_id,
                reason=sanction.reason,
                sanction_id=sanction.sanction_id,
                time=sanction.time,
                user_id=sanction.user_id)
            con.execute(clause)
        except Exception as err:
            print(err)

    @staticmethod
    def delete(sanction: Sanction):
        con, meta = Db.connect()
        t_sanction = meta.tables['sanctions']
        try:
            clause = t_sanction.delete().where(t_sanction.c.sanction_id == str(sanction.sanction_id))
            con.execute(clause)
        except Exception as err:
            print(err)

    @staticmethod
    def delete_from_user(user_id: int):
        con, meta = Db.connect()
        t_sanction = meta.tables['sanctions']
        try:
            clause = t_sanction.delete().where(t_sanction.c.user_id == str(user_id))
            con.execute(clause)
        except Exception as err:
            print(err)


class SanctionMethod:

    @staticmethod
    async def create_sanction(user, event, mod, guild, reason=None, time=None):
        id = int(datetime.now().strftime('%Y%m%d%H%M%S%f'))

        sanction = Sanction(id)

        sanction.user_id = user.id
        sanction.event = event
        sanction.moderator_id = mod.id
        sanction.guild_id = guild.id
        sanction.reason = reason
        sanction.time = time

        SanctionsDB.create_sanction(sanction)
        return sanction.sanction_id

    @staticmethod
    async def create_strike(user, event, guild, reason=None):
        id = int(datetime.now().strftime('%Y%m%d%H%M%S%f'))

        sanction = Sanction(id)

        sanction.user_id = user.id
        sanction.event = f"AutoMod | {event}"
        sanction.moderator_id = 456504213262827524
        sanction.guild_id = guild.id
        sanction.reason = reason
        sanction.time = None

        SanctionsDB.create_sanction(sanction)
        return sanction.sanction_id

    @staticmethod
    async def find_sanction_id(ctx, id):
        sanction = SanctionsDB.get_sanction(id)
        return sanction

    @staticmethod
    async def find_sanction_member(ctx, member: typing.Union[discord.Member, discord.User], guild: discord.Guild):
        sanction = SanctionsDB.get_sanctions_from_guild_user(guild, member)
        return sanction
