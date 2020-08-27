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

import psycopg2
from psycopg2 import extras
from sqlalchemy.sql.elements import and_

from modules.sql.dbConnect import Db
from modules.sql.guild import Guild


class RoleDB:

    @staticmethod
    def rows_to_dict(rows) -> dict:
        roles = {"guild_id": rows['guild_id'], "level": rows['level'], "role_id": rows['role_id']}
        return roles

    """
    Get methods
    """

    @staticmethod
    def get_one_from_level(level: int, guild_id: int):
        con, meta = Db.connect()
        t_roles = meta.tables['roles']
        try:
            clause = t_roles.select().where(
                and_(t_roles.c.level == level,
                     t_roles.c.guild_id == str(guild_id)))
            rows = con.execute(clause)
            row = rows.fetchone()
            if row:
                return RoleDB.rows_to_dict(row)
            return {}
        except Exception as err:
            print(err)

    @staticmethod
    def set_level(role_id: int, guild_id: int, level: int):
        con, meta = Db.connect()
        t_roles = meta.tables['roles']
        try:
            clause = t_roles.insert().values(
                guild_id=guild_id,
                role_id=role_id,
                level=level)
            con.execute(clause)
        except Exception as err:
            print(err)

    @staticmethod
    def unset_level(level: int, guild_id: int):
        con, meta = Db.connect()
        t_roles = meta.tables['roles']
        try:
            clause = t_roles.delete() \
                .where(
                and_(
                    t_roles.c.level == level,
                    t_roles.c.guild_id == str(guild_id)))
            con.execute(clause)

        except Exception as err:
            print(err)
