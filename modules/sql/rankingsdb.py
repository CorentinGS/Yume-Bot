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

import numpy as np
import pandas
import psycopg2
from psycopg2 import extras
from sqlalchemy import and_, select, func

from modules.sql.dbConnect import Db
from modules.sql.guild import Guild
from modules.sql.user import User


class RankingsDB:

    @staticmethod
    def rows_to_dict(rows) -> dict:
        rankings = {"guild_id": rows['guild_id'], "level": rows['level'], "xp": rows['xp'], "total": rows['total'],
                    "reach": rows['reach'], "user_id": rows['user_id']}
        return rankings

    @staticmethod
    def get_user(user: User, guild: Guild) -> dict:
        con, meta = Db.connect()
        t_rankings = meta.tables['rankings']
        try:
            clause = t_rankings.select().where(
                and_(t_rankings.c.user_id == str(user.user_id),
                     t_rankings.c.guild_id == str(guild.guild_id)))
            rows = con.execute(clause)
            row = rows.fetchone()
            if row:
                return RankingsDB.rows_to_dict(row)
            return {}
        except Exception as err:
            print(err)

    @staticmethod
    def ranking_exists(user: User, guild: Guild) -> bool:
        con, meta = Db.connect()
        t_rankings = meta.tables['rankings']
        try:
            clause = select([func.count()]).select_from(t_rankings).where(and_(
                t_rankings.c.guild_id == str(guild.guild_id),
                t_rankings.c.user_id == str(user.user_id)))
            rows = con.execute(clause)
            row = rows.fetchone()
            if row[0] > 0:
                return True
            return False
        except Exception as err:
            print(err)

    @staticmethod
    def create_ranking(user: User, guild: Guild):
        con, meta = Db.connect()
        t_rankings = meta.tables['rankings']
        try:
            clause = t_rankings.insert().values(
                guild_id=guild.guild_id,
                level=0,
                reach=20,
                total=0,
                user_id=user.user_id,
                xp=0)
            con.execute(clause)
        except Exception as err:
            print(err)

    @staticmethod
    def reset_user(user: User, guild: Guild):
        con, meta = Db.connect()
        t_rankings = meta.tables['rankings']
        try:
            clause = t_rankings.update().where(t_rankings.c.guild_id == str(guild.guild_id),
                                               t_rankings.c.user_id == str(user.user_id)) \
                .values(level=0,
                        reach=20,
                        total=0,
                        xp=0)
            con.execute(clause)
        except Exception as err:
            print(err)

    @staticmethod
    def update_user(user: User, guild: Guild, ranking: dict):
        con, meta = Db.connect()
        t_rankings = meta.tables['rankings']
        try:
            clause = t_rankings.update() \
                .where(
                and_(
                    t_rankings.c.guild_id == str(guild.guild_id),
                    t_rankings.c.user_id == str(user.user_id))) \
                .values(level=ranking["level"],
                        reach=ranking['reach'],
                        xp=ranking['xp'],
                        total=ranking['total'])
            con.execute(clause)
        except Exception as err:
            print(err)

    @staticmethod
    def update_user_id(user_id: id, guild_id: id, level: int, reach: int, xp: int):
        con, meta = Db.connect()
        t_rankings = meta.tables['rankings']
        try:
            clause = t_rankings.update() \
                .where(
                and_(
                    t_rankings.c.guild_id == str(guild_id),
                    t_rankings.c.user_id == str(user_id))) \
                .values(level=level,
                        reach=reach,
                        xp=xp)
            con.execute(clause)
        except Exception as err:
            print(err)

    @staticmethod
    def get_rank(user: User, guild: Guild) -> int:
        users = []
        con, meta = Db.connect()
        t_rankings = meta.tables['rankings']
        try:
            clause = select([t_rankings.c.user_id]) \
                .select_from(t_rankings) \
                .group_by(t_rankings.c.user_id, t_rankings.c.total) \
                .order_by(t_rankings.c.total.desc()) \
                .where(t_rankings.c.guild_id == str(guild.guild_id))
            rows = con.execute(clause)
            for row in rows:
                users.append(row[0])
            df = pandas.DataFrame(np.array(users), columns=["ID"])
            return df.ID[df.ID == user.user_id].index.tolist()[0] + 1
        except Exception as err:
            print(err)

    @staticmethod
    def get_scoreboard(guild: Guild) -> list:
        users = []
        con, meta = Db.connect()
        t_rankings = meta.tables['rankings']
        try:
            clause = select([t_rankings.c.user_id]) \
                .select_from(t_rankings) \
                .group_by(t_rankings.c.user_id, t_rankings.c.total) \
                .order_by(t_rankings.c.total.desc()) \
                .limit(10) \
                .where(t_rankings.c.guild_id == str(guild.guild_id))

            rows = con.execute(clause)
            for row in rows:
                users.append(row[0])
            df = pandas.DataFrame(np.array(users), columns=["ID"])
            return df.ID.values.tolist()
        except Exception as err:
            print(err)

    @staticmethod
    def get_all():
        con, meta = Db.connect()
        t_rankings = meta.tables['rankings']
        clause = t_rankings.select()
        rows = con.execute(clause)
        rankings = []
        for row in rows:
            rankings.append(RankingsDB.rows_to_dict(row))
        return rankings

    @staticmethod
    def set_ignored_chan(guild_id: int, chan_id: int):
        con, meta = Db.connect()
        t_rankings_chan = meta.tables['rankings_chan']
        try:
            clause = t_rankings_chan.insert().values(
                guild_id=guild_id, chan_id=chan_id)
            con.execute(clause)
        except Exception as err:
            print(err)

    @staticmethod
    def is_ignored_chan(chan_id: int):
        con, meta = Db.connect()
        t_rankings_chan = meta.tables['rankings_chan']
        try:
            clause = select([func.count()]) \
                .select_from(t_rankings_chan) \
                .where(t_rankings_chan.c.chan_id == str(chan_id))
            rows = con.execute(clause)
            row = rows.fetchone()
            if row[0] > 0:
                return True
            return False
        except Exception as err:
            print(err)

    @staticmethod
    def get_ignored_chan(guild_id: int):
        channels = []
        con, meta = Db.connect()
        t_rankings_chan = meta.tables['rankings_chan']
        try:
            clause = t_rankings_chan.select().where(t_rankings_chan.c.guild_id == str(guild_id))
            rows = con.execute(clause)
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
        con, meta = Db.connect()
        t_rankings_chan = meta.tables['rankings_chan']
        try:
            clause = t_rankings_chan.delete() \
                .where(
                and_(
                    t_rankings_chan.c.chan_id == str(chan_id),
                    t_rankings_chan.c.guild_id == str(guild_id)))
            con.execute(clause)
        except Exception as err:
            print(err)
