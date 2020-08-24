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

from modules.sql.dbConnect import Db
from modules.sql.guild import Guild
from modules.sql.user import User

try:
    con = psycopg2.connect("host=postgre dbname=yumebot port=5432 user=postgres password=yumebot")
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
except psycopg2.DatabaseError as e:
    print('Error %s' % e)


class MuteDB:
    """
    Get methods
    """

    """
    Check methods
    """

    @staticmethod
    def is_muted(user: User, guild: Guild):
        con, meta = Db.connect()
        t_muted = meta.tables['muted']
        try:
            clause = t_muted.select().where(
                t_muted.and_(t_muted.c.user_id == str(user.user_id), t_muted.c.guild_id == str(guild.guild_id)))
            rows = con.execute(clause)
            if rows:
                return True
            return False
        except Exception as err:
            print(err)

    """
     Set / Unset methods
     """

    @staticmethod
    def set_mute(user: User, guild: Guild):
        con, meta = Db.connect()
        t_muted = meta.tables['muted']
        try:
            clause = t_muted.insert().values(
                guild_id=guild.guild_id,
                user_id=user.user_id
            )
            con.execute(clause)
        except Exception as err:
            print(err)

    @staticmethod
    def unset_mute(user: User, guild: Guild):
        con, meta = Db.connect()
        t_muted = meta.tables['muted']
        try:
            clause = t_muted.delete().where(
                t_muted._and(t_muted.c.user_id == str(user.user_id), t_muted.c.guild_id == str(guild.guild_id)))
            con.execute(clause)
        except Exception as err:
            print(err)
