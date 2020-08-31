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
import pandas
import numpy as np

from modules.sql.dbConnect import Db
from model.guild import Guild


class GuildDB:
    @staticmethod
    def guild_from_row(rows):
        return Guild(rows['guild_id'], rows['blacklist'], rows['color'], rows['greet'], rows['greet_chan'],
                     rows['log_chan'], rows['logging'], rows['setup'],
                     rows['vip'])

    @staticmethod
    def guilds_from_row(rows):
        guilds = []
        for row in rows:
            guilds.append(GuildDB.guild_from_row(row))
        return guilds

    @staticmethod
    def get_one(guild_id: int) -> Guild:
        con, cur = Db.connect()
        try:
            cur.execute("SELECT * FROM public.guild WHERE guild_id = {}::text;".format(str(guild_id)))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            return GuildDB.guild_from_row(rows)
        else:
            g = Guild(guild_id)
            GuildDB.create(g)
            return g

    """
    Create & delete methods
    """

    @staticmethod
    def create(guild: Guild):
        con, cur = Db.connect()
        try:
            cur.execute(
                "INSERT INTO public.guild ( blacklist, color, greet, greet_chan, guild_id, log_chan, logging, setup, vip) "
                " VALUES ( %s, %s, %s, %s::text, %s::text, %s::text, %s, %s, %s);",
                (guild.blacklist, guild.color, guild.greet, str(guild.greet_chan), str(guild.guild_id),
                 str(guild.log_chan),
                 guild.logging,
                 guild.setup, guild.vip))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def delete(guild: Guild):
        con, cur = Db.connect()
        try:
            cur.execute("DELETE FROM public.guild WHERE guild_id = {}::text;".format(str(guild.guild_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    """
    Update methods
    """

    @staticmethod
    def update_guild(guild: Guild):
        con, cur = Db.connect()
        try:
            cur.execute(
                "UPDATE public.guild SET blacklist = '{}', color = '{}', greet = '{}',"
                " greet_chan = '{}::text', log_chan = '{}::text', logging = '{}', "
                "setup = '{}', vip = '{}'  WHERE  guild_id = {}::text".format(
                    guild.blacklist, guild.color, guild.greet, str(guild.greet_chan), str(guild.log_chan),
                    guild.logging,
                    guild.setup,
                    guild.vip, str(guild.guild_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    """
    Others methods
    """

    @staticmethod
    def exists_in_admin(role_id, guild_id: int) -> bool:
        con, cur = Db.connect()
        try:
            cur.execute(
                "SELECT count(*) FROM public.admin WHERE guild_id = {}::text AND role_id = {}::text".format(
                    str(guild_id),
                    str(role_id)))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows[0] > 0:
            return True
        return False

    @staticmethod
    def remove_admin(role_id, guild_id: int):
        con, cur = Db.connect()
        try:
            cur.execute(
                "DELETE FROM public.admin WHERE guild_id = {}::text AND role_id = {}::text".format(str(guild_id), str(role_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def set_admin(role_id: int, guild_id: int):
        con, cur = Db.connect()
        try:
            cur.execute(
                "INSERT INTO public.admin ( guild_id, role_id, admin ) VALUES ( %s::text, %s::text, %s)",
                (str(guild_id), str(role_id),
                 True))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def set_mod(role_id: int, guild_id: int):
        con, cur = Db.connect()
        try:
            cur.execute(
                "INSERT INTO public.admin ( guild_id, role_id, admin ) VALUES ( %s::text, %s::text, %s)",
                (str(guild_id), str(role_id),
                 False))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def get_admin_roles(guild: Guild) -> list:
        con, cur = Db.connect()
        try:
            cur.execute(
                "SELECT role_id FROM public.admin WHERE guild_id = {}::text AND admin = true".format(str(guild.guild_id)))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchall()
        if rows:
            df = pandas.DataFrame(np.array(rows))
            return df[0].values.tolist()
        return []

    @staticmethod
    def get_mod_roles(guild: Guild) -> list:
        con, cur = Db.connect()
        try:
            cur.execute(
                "SELECT role_id FROM public.admin WHERE guild_id = {}::text AND admin = false".format(str(guild.guild_id)))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchall()
        if rows:
            df = pandas.DataFrame(np.array(rows))
            return df[0].values.tolist()
        return []
