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

from datetime import datetime

import psycopg2
from psycopg2 import extras
from pytz import timezone

from modules.sql.user import User

try:
    con = psycopg2.connect("host=postgre dbname=yumebot port=5432 user=postgres")
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
except psycopg2.DatabaseError as e:
    print('Error %s' % e)


class BlacklistDB:
    """
    Get methods
    """

    @staticmethod
    def get_one(user_id: int):
        cur.execute("SELECT * FROM public.blacklist WHERE user_id = {};".format(user_id))
        rows = cur.fetchone()
        if rows:
            return rows
        return "Error : User not found"

    @staticmethod
    def get_user(user: User):
        cur.execute("SELECT * FROM public.blacklist WHERE user_id = {};".format(user.user_id))
        rows = cur.fetchone()
        if rows:
            return rows
        return "Error : User not found"

    """
    Check methods
    """

    @staticmethod
    def is_blacklist(user: User):
        cur.execute(
            "SELECT * FROM public.blacklist WHERE user_id = {}".format(user.user_id))
        rows = cur.fetchone()
        if rows:
            return True
        return False

    """
    Set / Unset methods
    """

    @staticmethod
    def set_blacklist(user: User, reason):
        cur.execute(
            "INSERT INTO public.blacklist ( reason, time, user_id) VALUES ( {}, {}, {} );".format(reason, datetime.now(
                timezone('UTC')), user.user_id)
        )
        con.commit()


    @staticmethod
    def unset_blacklist(user: User):
        cur.execute("DELETE FROM public.blacklist WHERE user_id = {};)".format(user.user_id))
        con.commit()
