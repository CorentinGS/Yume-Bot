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
        return Sanction(rows['sanction_id'], rows['event'], rows['guild_id'], rows['moderator_id'], rows['reason'],
                        rows['time'], rows['user_id'], rows['event_date'])

    @staticmethod
    def sanctions_from_row(rows):
        sanctions = []
        for row in rows:
            sanctions.append(SanctionsDB.sanction_from_row(row))
        return sanctions

    """
    Get methods
    """

    @staticmethod
    def get_sanction(sanction_id: int) -> Sanction:
        con, cur = Db.connect()
        try:
            cur.execute("SELECT * FROM public.sanctions WHERE sanction_id = {}::text;".format(str(sanction_id)))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            return SanctionsDB.sanction_from_row(rows)

    @staticmethod
    def get_sanctions_from_guild_user(guild_id: int, user_id: int) -> list:
        con, cur = Db.connect()
        try:
            cur.execute(
                "SELECT * FROM public.sanctions WHERE user_id = {}::text AND guild_id = {}::text;".format(str(user_id),
                                                                                                          str(
                                                                                                              guild_id)))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchall()
        if rows:
            return SanctionsDB.sanctions_from_row(rows)

        return []

    """
    Create & delete methods
    """

    @staticmethod
    def create_sanction(sanction: Sanction):
        con, cur = Db.connect()
        try:
            cur.execute(
                "INSERT INTO public.sanctions ( event, event_date, guild_id, moderator_id, reason, sanction_id, time, user_id) \
                VALUES ( %s, %s, %s::text, %s::text, %s, %s::text, %s, %s::text );", (
                    sanction.event, str(sanction.event_date), str(sanction.guild_id), str(sanction.moderator_id),
                    sanction.reason,
                    str(sanction.sanction_id), sanction.time, str(sanction.user_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def delete(sanction: Sanction):
        con, cur = Db.connect()
        try:
            cur.execute("DELETE FROM public.sanctions WHERE sanction_id = {}::text;".format(str(sanction.sanction_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def delete_from_user(user_id: int):
        con, cur = Db.connect()
        try:
            cur.execute("DELETE FROM public.sanctions WHERE user_id = {}::text;".format(str(user_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()


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
        sanction = SanctionsDB.get_sanctions_from_guild_user(guild.id, member.id)
        return sanction
