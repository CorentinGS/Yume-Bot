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

from sqlalchemy import and_, select, func

from modules.sql.dbConnect import Db


class MuteDB:


    """
    Check methods
    """

    @staticmethod
    def is_muted(user_id: int, guild_id: int):
        con, cur = Db.connect()
        try:
            cur.execute(
                "SELECT * FROM public.muted WHERE user_id = {}::text and guild_id = {}::text;".format(str(user_id), str(guild_id)))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            return True
        return False

    """
     Set / Unset methods
     """

    @staticmethod
    def set_mute(user_id: int, guild_id: int):
        con, cur = Db.connect()
        try:
            cur.execute(
                "INSERT INTO public.muted ( guild_id, user_id) VALUES ( {}::text, {}::text );".format(str(guild_id), str(user_id))
            )
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def unset_mute(user_id: int, guild_id: int):
        con, cur = Db.connect()
        try:
            cur.execute(
                "DELETE FROM public.muted WHERE user_id = {}::text and guild_id = {}::text;".format(str(user_id), str(guild_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()
