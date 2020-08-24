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
from sqlalchemy import select, func

from modules.sql.dbConnect import Db
from modules.sql.guild import Guild


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
        con, meta = Db.connect()
        t_guild = meta.tables['guild']
        try:
            clause = t_guild.select().where(t_guild.c.guild_id == str(guild_id))
            for row in con.execute(clause):
                if row:
                    return GuildDB.guild_from_row(row)
                else:
                    g = Guild(guild_id)
                    GuildDB.create(g)
                    return g
        except Exception as err:
            print(err)

    """
    Checks methods
    """

    @staticmethod
    def has_blacklist(guild: Guild) -> bool:
        con, meta = Db.connect()
        t_guild = meta.tables['guild']
        try:
            clause = t_guild.select([t_guild.c.blacklist]).where(t_guild.c.guild_id == str(guild.guild_id))
            for row in con.execute(clause):
                if row:
                    return row[0]
                return False
        except Exception as err:
            print(err)

    @staticmethod
    def has_logging(guild: Guild) -> bool:
        con, meta = Db.connect()
        t_guild = meta.tables['guild']
        try:
            clause = t_guild.select([t_guild.c.logging]).where(t_guild.c.guild_id == str(guild.guild_id))
            for row in con.execute(clause):
                if row:
                    return row[0]
                return False
        except Exception as err:
            print(err)

    """
    Create & delete methods
    """

    @staticmethod
    def create(guild: Guild):
        con, meta = Db.connect()
        t_guild = meta.tables['guild']
        try:
            clause = t_guild.insert().values(
                blacklist=guild.blacklist,
                color=guild.color,
                greet=guild.greet,
                greet_chan=guild.greet_chan,
                guild_id=guild.guild_id,
                log_chan=guild.log_chan,
                logging=guild.logging,
                setup=guild.setup,
                vip=guild.vip)
            con.execute(clause)
        except Exception as err:
            print(err)

    @staticmethod
    def delete(guild: Guild):
        con, meta = Db.connect()
        t_guild = meta.tables['guild']
        try:
            clause = t_guild.delete().where(t_guild.c.guild_id == str(guild.guild_id))
            con.execute(clause)
        except Exception as err:
            print(err)

    """
    Update methods
    """

    @staticmethod
    def update_guild(guild: Guild):
        con, meta = Db.connect()
        t_guild = meta.tables['guild']
        try:
            clause = t_guild.update().where(t_guild.c.guild_id == str(guild.guild_id)).values(
                blacklist=guild.blacklist,
                color=guild.color,
                greet=guild.greet,
                greet_chan=guild.greet_chan,
                guild_id=guild.guild_id,
                log_chan=guild.log_chan,
                logging=guild.logging,
                setup=guild.setup,
                vip=guild.vip)
            con.execute(clause)
        except Exception as err:
            print(err)

    """
    Others methods
    """

    @staticmethod
    def exists_in_admin(role_id, guild: Guild) -> bool:
        con, meta = Db.connect()
        t_admin = meta.tables['admin']
        try:
            clause = select([func.count()]).select_from(t_admin).where(t_admin.and_(
                t_admin.c.guild_id == guild.guild_id,
                t_admin.c.role_id == role_id))
            for row in con.execute(clause):
                if row[0] > 0:
                    return True
                return False
        except Exception as err:
            print(err)

    @staticmethod
    def remove_admin(role_id, guild: Guild):
        con, meta = Db.connect()
        t_admin = meta.tables['admin']
        try:
            clause = t_admin.delete().where(
                t_admin.c.guild_id == guild.guild_id,
                t_admin.c.role_id == role_id)
            con.execute(clause)
        except Exception as err:
            print(err)

    @staticmethod
    def set_admin(role_id: int, guild_id: int):
        con, meta = Db.connect()
        t_admin = meta.tables['admin']
        try:
            clause = t_admin.insert().values(
                guild_id=guild_id,
                role_id=role_id,
                admin=True
            )
            con.execute(clause)
        except Exception as err:
            print(err)

    @staticmethod
    def set_mod(role_id: int, guild_id: int):
        con, meta = Db.connect()
        t_admin = meta.tables['admin']
        try:
            clause = t_admin.insert().values(
                guild_id=guild_id,
                role_id=role_id,
                admin=False
            )
            con.execute(clause)
        except Exception as err:
            print(err)

    @staticmethod
    def is_mod(role_id: int, guild: Guild) -> bool:
        con, meta = Db.connect()
        t_admin = meta.tables['admin']
        try:
            clause = t_admin.select([t_admin.c.admin]).where(t_admin.and_(t_admin.c.guild_id == str(guild.guild_id),
                                                                          t_admin.c.role_id == str(role_id)))
            for row in con.execute(clause):
                if row['admin'] is False:
                    return True
                return False
        except Exception as err:
            print(err)

    @staticmethod
    def get_admin_roles(guild: Guild) -> list:
        con, meta = Db.connect()
        t_admin = meta.tables['admin']
        try:
            clause = t_admin.select([t_admin.c.role_id]).where(t_admin.and_(t_admin.c.guild_id == str(guild.guild_id),
                                                                            t_admin.c.admin == True))
            for row in con.execute(clause):
                if row:
                    df = pandas.DataFrame(np.array(row))
                    return df[0].values.tolist()
                return []
        except Exception as err:
            print(err)

    @staticmethod
    def get_mod_roles(guild: Guild) -> list:
        con, meta = Db.connect()
        t_admin = meta.tables['admin']
        try:
            clause = t_admin.select([t_admin.c.role_id]).where(t_admin.and_(t_admin.c.guild_id == str(guild.guild_id),
                                                                            t_admin.c.admin == False))
            for row in con.execute(clause):
                if row:
                    df = pandas.DataFrame(np.array(row))
                    return df[0].values.tolist()
                return []
        except Exception as err:
            print(err)
