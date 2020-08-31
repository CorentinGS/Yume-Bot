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
import json

import numpy as np
import pandas
import psycopg2
from sqlalchemy import and_, select, func

from modules.sql.dbConnect import Db
from model.guild import Guild
from model.user import User
from psycopg2 import extras


class RankingsDB:

    @staticmethod
    def rows_to_dict(rows) -> dict:
        rankings = {"guild_id": rows['guild_id'], "level": rows['level'], "xp": rows['xp'], "total": rows['total'],
                    "reach": rows['reach'], "user_id": rows['user_id']}
        return rankings

    @staticmethod
    def get_user(user_id: int, guild_id: int) -> dict:
        con, cur = Db.connect()
        try:
            cur.execute(
                "SELECT * FROM public.rankings WHERE user_id = {}::text and guild_id = {}::text;".format(str(user_id),
                                                                                                         str(guild_id)))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            rankings = RankingsDB.rows_to_dict(rows)
            return rankings
        return {}

    @staticmethod
    def create_ranking(user_id: int, guild_id: int):
        con, cur = Db.connect()
        try:
            cur.execute(
                "INSERT INTO public.rankings ( guild_id, level, reach, total, user_id, xp) "
                " VALUES ( {}::text, 0, 20, 0, {}::text, 0 );".format(
                    str(guild_id), str(user_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def reset_user(user_id: int, guild_id: int):
        con, cur = Db.connect()
        try:
            cur.execute(
                "UPDATE public.rankings SET level = 0, reach = 20, total = 0, xp = 0 "
                "WHERE guild_id = {}::text AND user_id = {}::text;".format(
                    str(guild_id), str(user_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def update_user(user_id: int, guild_id: int, ranking: dict):
        con, cur = Db.connect()
        try:
            cur.execute(
                "UPDATE public.rankings SET level = {}, reach = {}, total = {}, xp = {} "
                "WHERE guild_id = {}::text AND user_id = {}::text;".format(
                    ranking['level'], ranking['reach'], ranking['total'], ranking['xp'],
                    str(guild_id), str(user_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def update_user_id(user_id: id, guild_id: id, level: int, reach: int, xp: int):
        con, cur = Db.connect()
        try:
            cur.execute(
                "UPDATE public.rankings SET level = {}, reach = {}, xp = {} "
                "WHERE guild_id = {}::text AND user_id = {}::text;".format(
                    level, reach, xp, str(guild_id), str(user_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def get_rank(user_id: int, guild_id: int) -> int:
        con, cur = Db.connect()
        try:
            cur.execute(
                "SELECT user_id FROM public.rankings "
                "WHERE guild_id = {}::text GROUP BY user_id, total ORDER BY total DESC "
                    .format(str(guild_id)))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchall()
        if rows:
            df = pandas.DataFrame(np.array(rows), columns=["ID"])
            return df.ID[df.ID == str(user_id)].index.tolist()[0] + 1
        return 0

    @staticmethod
    def get_scoreboard(guild: Guild) -> list:
        con, cur = Db.connect()
        try:
            cur.execute(
                "SELECT user_id FROM public.rankings "
                "WHERE guild_id = {}::text GROUP BY user_id, total ORDER BY total DESC LIMIT 10".format(
                    str(guild.guild_id)))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchall()
        if rows:
            df = pandas.DataFrame(np.array(rows), columns=["ID"])
            return df.ID.values.tolist()
        return []

    @staticmethod
    def get_all():
        con, cur = Db.connect()
        try:
            cur.execute(
                "SELECT * FROM public.rankings;")
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchall()
        if rows:
            rankings = []
            for row in rows:
                rankings.append(RankingsDB.rows_to_dict(row))
            return rankings

    @staticmethod
    def set_ignored_chan(guild_id: int, chan_id: int):
        con, cur = Db.connect()
        try:
            cur.execute(
                "INSERT INTO public.rankings_chan ( guild_id, chan_id) VALUES ({}::text , {}::text );".format(
                    str(guild_id), str(chan_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def is_ignored_chan(chan_id: int):
        con, cur = Db.connect()
        try:
            cur.execute(
                "SELECT * FROM public.rankings_chan WHERE chan_id = {}::text;".format(str(chan_id))
            )
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            return True
        return False

    @staticmethod
    def get_ignored_chan(guild_id: int):
        channels = []
        con, cur = Db.connect()
        try:
            cur.execute(
                "SELECT FROM public.rankings_chan WHERE guild_id = {}::text".format(str(guild_id))
            )
            rows = cur.fetchall()
            if rows:
                for row in rows:
                    channels.append({
                        "chan_id": row['chan_id'],
                        "guild_id": row["guild_id"]
                    })
            return channels

        except Exception as err:
            print(err)

    @staticmethod
    def delete_ignored_chan(guild_id: int, chan_id: int):
        con, cur = Db.connect()
        try:
            cur.execute(
                "DELETE FROM public.rankings_chan WHERE	guild_id = {}::text AND chan_id = {}::text;".format(
                    str(guild_id), str(chan_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()
