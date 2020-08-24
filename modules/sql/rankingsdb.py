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

from modules.sql.guild import Guild
from modules.sql.user import User

try:
    con = psycopg2.connect("host=postgre dbname=yumebot port=5432 user=postgres password=yumebot")
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
except psycopg2.DatabaseError as e:
    print('Error %s' % e)


class RankingsDB:

    @staticmethod
    def rows_to_dict(rows) -> dict:
        rankings = {"level": rows['level'], "xp": rows['xp'], "total": rows['total'], "guild_id": rows['guild_id'],
                    "reach": rows['reach'], "user_id": rows['user_id']}
        return rankings

    @staticmethod
    def rankings_from_rows(rows) -> list:
        rankings = []
        for row in rows:
            rankings.append(RankingsDB.rows_to_dict(row))
        return rankings

    """
    Get methods
    """

    @staticmethod
    def get_one(user_id: int, guild_id: int) -> dict:
        try:
            cur.execute("SELECT * FROM public.rankings WHERE user_id = {} and guild_id = {};".format(str(user_id),
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
    def get_user(user: User, guild: Guild) -> dict:
        try:
            cur.execute(
                "SELECT * FROM public.rankings WHERE user_id = {} and guild_id = {};".format(str(user.user_id),
                                                                                             str(guild.guild_id)))
        except Exception as err:
            print(err)
            con.rollback()
        try:
            rows = cur.fetchone()
        except (Exception, psycopg2.Error) as error:
            return {}
        else:
            if rows:
                rankings = RankingsDB.rows_to_dict(rows)
                return rankings

            return {}

    @staticmethod
    def ranking_exists(user: User, guild: Guild) -> bool:
        try:
            cur.execute(
                "SELECT count(*) FROM public.rankings WHERE user_id = {} AND guild_id = {};".format(str(user.user_id),
                                                                                                    str(
                                                                                                        guild.guild_id)))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows[0] > 0:
            return True
        return False

    """
    Create methods
    """

    @staticmethod
    def create_ranking(user: User, guild: Guild):
        try:
            cur.execute(
                "INSERT INTO public.rankings ( guild_id, level, reach, total, user_id, xp)  VALUES ( {}, 0, 20, 0, {}, 0 );".format(
                    str(guild.guild_id), str(user.user_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def reset_user(user: User, guild: Guild):
        try:
            cur.execute(
                "UPDATE public.rankings SET level = 0, reach = 20, total = 0, xp = 0 WHERE guild_id = {} AND user_id = {};".format(
                    str(guild.guild_id), str(user.user_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    """
    Level methods
    """

    @staticmethod
    def update_user(user: User, guild: Guild, ranking: dict):
        try:
            cur.execute(
                "UPDATE public.rankings SET level = {}, reach = {}, total = {}, xp = {} WHERE guild_id = {} AND user_id = {};".format(
                    ranking['level'], ranking['reach'], ranking['total'], ranking['xp'],
                    str(guild.guild_id), str(user.user_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def update_user_id(user: id, guild: id, level: int, reach: int, xp: int):
        try:
            cur.execute(
                "UPDATE public.rankings SET level = {}, reach = {}, xp = {} WHERE guild_id = {} AND user_id = {};".format(
                    level, reach, xp, str(guild), str(user)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def get_rank(user: User, guild: Guild) -> int:
        try:
            cur.execute(
                "SELECT user_id FROM public.rankings WHERE guild_id = {} GROUP BY user_id, total ORDER BY total DESC ".format(
                    str(guild.guild_id)))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchall()
        if rows:
            df = pandas.DataFrame(np.array(rows), columns=["ID"])
            return df.ID[df.ID == user.user_id].index.tolist()[0] + 1
        return 0

    @staticmethod
    def get_scoreboard(guild: Guild) -> list:
        try:
            cur.execute(
                "SELECT user_id FROM public.rankings WHERE guild_id = {} GROUP BY user_id, total ORDER BY total DESC LIMIT 10".format(
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
        try:
            cur.execute(
                "SELECT * FROM public.rankings;")
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchall()
        if rows:
            return RankingsDB.rankings_from_rows(rows)

    @staticmethod
    def set_ignored_chan(guild_id: int, chan_id: int):
        try:
            cur.execute(
                "INSERT INTO public.rankings_chan ( guild_id, chan_id) VALUES ({} , {} );".format(str(guild_id),
                                                                                                  str(chan_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def is_ignored_chan(chan_id: int):
        try:
            cur.execute(
                "SELECT * FROM public.rankings_chan WHERE chan_id = CAST({} AS varchar);".format(chan_id)
            )
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            return True
        return False

    @staticmethod
    def get_ignored_chans(guild_id: int):
        return

    @staticmethod
    def delete_ignored_chan(guild_id: int, chan_id: int):
        try:
            cur.execute(
                "DELETE FROM public.rankings_chan WHERE	guild_id = {} AND chan_id = {};".format(str(guild_id),
                                                                                                   str(chan_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()
