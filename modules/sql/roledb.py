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

#
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#
import psycopg2
from psycopg2 import extras

from modules.sql.guild import Guild

try:
    con = psycopg2.connect("host=postgre dbname=yumebot port=5432 user=postgres password=yumebot")
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
except psycopg2.DatabaseError as e:
    print('Error %s' % e)


class RoleDB:
    """
    Get methods
    """

    @staticmethod
    def get_one_from_role(role_id: int, guild: Guild):
        try:
            cur.execute(
                "SELECT * FROM public.roles WHERE role_id = {} and guild_id = {};".format(role_id, guild.guild_id))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            return rows

    @staticmethod
    def get_one_from_level(level: int, guild: Guild):
        try:
            cur.execute("SELECT * FROM public.roles WHERE level = {} and guild_id = {};".format(level, guild.guild_id))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            return rows

    """
    Check methods
    """

    @staticmethod
    def set_level(role_id: int, guild: Guild, level: int):
        try:
            cur.execute(
                "INSERT INTO public.roles ( guild_id, role_id, level) VALUES ( {}, {}, {} );".format(guild.guild_id,
                                                                                                     role_id, level)
            )
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def unset_level(level: int, guild: Guild):
        try:
            cur.execute(
                "DELETE FROM public.roles WHERE level = {} and guild_id = {};".format(level, guild.guild_id))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()
