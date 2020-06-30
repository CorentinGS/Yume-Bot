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
import pandas as pandas
import psycopg2
from psycopg2 import extras

from modules.sql.guild import Guild

try:
    con = psycopg2.connect("host=postgre dbname=yumebot port=5432 user=postgres password=yumebot")
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
except psycopg2.DatabaseError as e:
    print('Error %s' % e)


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
        try:
            cur.execute("SELECT * FROM public.guild WHERE guild_id = {};".format(guild_id))
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

    @staticmethod
    def get_guild(guild: Guild) -> Guild:
        try:
            cur.execute("SELECT * FROM public.guild WHERE guild_id = {};".format(guild.guild_id))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            return GuildDB.guild_from_row(rows)
        else:
            GuildDB.create(guild)
            return guild

    @staticmethod
    def get_all() -> list:
        try:
            cur.execute("SELECT * FROM public.guild;")
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchall()
        if rows:
            return GuildDB.guilds_from_row(rows)
        return []

    """
    Checks methods
    """

    @staticmethod
    def is_vip(guild: Guild) -> bool:
        try:
            cur.execute('SELECT vip FROM public.guild WHERE guild_id = {};'.format(guild.guild_id))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            return rows[0]
        return False

    @staticmethod
    def is_setup(guild: Guild) -> bool:
        try:
            cur.execute('SELECT setup FROM public.guild WHERE guild_id = {};'.format(guild.guild_id))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            return rows[0]
        return False

    @staticmethod
    def has_blacklist(guild: Guild) -> bool:
        try:
            cur.execute('SELECT blacklist FROM public.guild WHERE guild_id = {};'.format(guild.guild_id))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            return rows[0]
        return False

    @staticmethod
    def has_logging(guild: Guild) -> bool:
        try:
            cur.execute('SELECT logging FROM public.guild WHERE guild_id = {};'.format(guild.guild_id))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            return rows[0]
        return False

    @staticmethod
    def guild_exists(guild: Guild) -> bool:
        try:
            cur.execute("SELECT count(*) FROM public.guild WHERE guild_id = {};".format(guild.guild_id))
        except Exception as err:
            print(err)
            con.rollback()
        try:
            rows = cur.fetchone()
        except psycopg2.ProgrammingError:
            return False
        else:
            return True

    """
    Create & delete methods
    """

    @staticmethod
    def create(guild: Guild):
        try:
            cur.execute(
                "INSERT INTO public.guild ( blacklist, color, greet, greet_chan, guild_id, log_chan, logging, setup, vip)  VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s);",
                (guild.blacklist, guild.color, guild.greet, guild.greet_chan, guild.guild_id, guild.log_chan,
                 guild.logging,
                 guild.setup, guild.vip))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def delete(guild: Guild):
        try:
            cur.execute("DELETE FROM public.guild WHERE guild_id = {};".format(guild.guild_id))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    """
    Update methods
    """

    @staticmethod
    def update_guild(guild: Guild):
        try:
            cur.execute(
                "UPDATE public.guild SET blacklist = '{}', color = '{}', greet = '{}', greet_chan = '{}', log_chan = '{}', logging = '{}', setup = '{}', vip = '{}'  WHERE  guild_id = {}".format(
                    guild.blacklist, guild.color, guild.greet, guild.greet_chan, guild.log_chan, guild.logging,
                    guild.setup,
                    guild.vip, guild.guild_id))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    """
    Set methods
    """

    @staticmethod
    def set_vip(guild: Guild):
        try:
            cur.execute("UPDATE public.guild SET vip = TRUE WHERE  guild_id = {}".format(guild.guild_id))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def set_blacklist(guild: Guild):
        try:
            cur.execute("UPDATE public.guild SET blacklist = TRUE WHERE  guild_id = {}".format(guild.guild_id))
        except Exception as err:
            print(err)
            con.rollback()

        con.commit()

    """
    Unset methods
    """

    @staticmethod
    def unset_vip(guild: Guild):
        try:
            cur.execute("UPDATE public.guild SET vip = FALSE WHERE guild_id = {}".format(guild.guild_id))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def unset_blacklist(guild: Guild):
        try:
            cur.execute("UPDATE public.guild SET blacklist = FALSE WHERE guild_id = {}".format(guild.guild_id))
        except Exception as err:
            print(err)
            con.rollback()

        con.commit()

    """
    Others methods
    """

    @staticmethod
    def is_admin(role_id: int, guild: Guild) -> bool:
        try:
            cur.execute(
                "SELECT admin FROM public.admin WHERE guild_id = {} AND role_id = {}".format(guild.guild_id, role_id))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            return rows['admin']
        return False

    @staticmethod
    def exists_in_admin(role_id, guild: Guild) -> bool:
        try:
            cur.execute(
                "SELECT count(*) FROM public.admin WHERE guild_id = {} AND role_id = {}".format(guild.guild_id,
                                                                                                role_id))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows[0] > 0:
            return True
        return False

    @staticmethod
    def remove_admin(role_id, guild: Guild):
        try:
            cur.execute("DELETE FROM public.admin WHERE guild_id = {} AND role_id = {}".format(guild.guild_id, role_id))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def set_admin(role_id: int, guild_id: int):
        try:
            cur.execute(
                "INSERT INTO public.admin ( guild_id, role_id, admin ) VALUES ( %s, %s, %s)", (guild_id, role_id,
                                                                                               True))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def set_mod(role_id: int, guild_id: int):
        try:
            cur.execute(
                "INSERT INTO public.admin ( guild_id, role_id, admin ) VALUES ( %s, %s, %s)", (guild_id, role_id,
                                                                                               False))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def is_mod(role_id: int, guild: Guild) -> bool:
        try:
            cur.execute(
                "SELECT admin FROM public.admin WHERE guild_id = {} AND role_id = {}".format(guild.guild_id, role_id))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows['admin'] is False:
            return True
        return False

    @staticmethod
    def get_admin_roles(guild: Guild) -> list:
        try:
            cur.execute("SELECT role_id FROM public.admin WHERE guild_id = {} AND admin = true".format(guild.guild_id))
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
        try:
            cur.execute("SELECT role_id FROM public.admin WHERE guild_id = {} AND admin = false".format(guild.guild_id))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchall()
        if rows:
            df = pandas.DataFrame(np.array(rows))
            return df[0].values.tolist()
        return []
