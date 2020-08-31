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

from sqlalchemy.sql.elements import and_

from modules.sql.dbConnect import Db


class RoleDB:

    @staticmethod
    def rows_to_dict(rows) -> dict:
        roles = {"guild_id": rows['guild_id'], "level": rows['level'], "role_id": rows['role_id']}
        return roles

    @staticmethod
    def get_one_from_level(level: int, guild_id: int):
        con, cur = Db.connect()
        try:
            cur.execute(
                "SELECT * FROM public.roles WHERE level = {} and guild_id = {}::text;".format(level, str(guild_id)))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            return rows

    @staticmethod
    def get_levels(guild_id: int):
        roles = []
        con, cur = Db.connect()
        try:
            cur.execute("SELECT * FROM public.roles WHERE guild_id = {}::text;".format(str(guild_id)))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchall()
        if rows:
            for row in rows:
                roles.append(RoleDB.rows_to_dict(row))
            return roles
        return []

    @staticmethod
    def set_level(role_id: int, guild_id: int, level: int):
        con, cur = Db.connect()
        try:
            cur.execute(
                "INSERT INTO public.roles ( guild_id, role_id, level) VALUES ( {}::text, {}::text, {} );".format(
                    str(guild_id),
                    str(role_id), level)
            )
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def unset_level(level: int, guild_id: int):
        con, cur = Db.connect()
        try:
            cur.execute(
                "DELETE FROM public.roles WHERE level = {} and guild_id = {}::text;".format(level, str(guild_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()
