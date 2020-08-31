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


from modules.sql.dbConnect import Db
from model.user import User


class UserDB:

    @staticmethod
    def user_from_row(rows):
        return User(rows['user_id'], rows['vip'], rows['crew'], rows['description'], rows['married'], rows["lover"])

    @staticmethod
    def users_from_row(rows):
        users = []
        for row in rows:
            users.append(UserDB.user_from_row(row))
        return users

    """
    Get methods
    """

    @staticmethod
    def get_one(user_id: int) -> User:
        con, cur = Db.connect()
        try:
            cur.execute("SELECT * FROM public.user WHERE user_id = {}::text;".format(str(user_id)))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            return UserDB.user_from_row(rows)
        else:
            u = User(user_id)
            UserDB.create(u)
            return u

    @staticmethod
    def get_vips():
        con, cur = Db.connect()
        try:
            cur.execute("SELECT * FROM public.user WHERE vip = TRUE")
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchall()
        if rows:
            return UserDB.users_from_row(rows)
        return "Error : No VIP"

    @staticmethod
    def create(user: User):
        con, cur = Db.connect()
        try:
            cur.execute("INSERT INTO public.user ( crew, description, user_id, vip) VALUES ( %s, %s, %s::text, %s);",
                        (user.crew, user.description, str(user.user_id), str(user.vip)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    """
    Set methods
    """

    @staticmethod
    def set_vip(user_id: int):
        con, cur = Db.connect()
        try:
            cur.execute("UPDATE public.user SET vip = TRUE WHERE  user_id = {}::text".format(str(user_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def set_lover(user_id: int, lover_id: int):
        con, cur = Db.connect()
        try:
            cur.execute("UPDATE public.user SET married = TRUE , lover = {}::text WHERE  user_id = {}::text".format(
                str(lover_id),
                str(user_id)))
            cur.execute("UPDATE public.user SET married = TRUE , lover = {}::text WHERE  user_id = {}::text".format(
                str(user_id),
                str(lover_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    """
    Unset methods
    """

    @staticmethod
    def unset_vip(user_id: int):
        con, cur = Db.connect()
        try:
            cur.execute("UPDATE public.user SET vip = FALSE WHERE  user_id = {}::text".format(str(user_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def unset_lover(user_id: int, lover_id: int):
        con, cur = Db.connect()
        try:
            cur.execute("UPDATE public.user SET married = FALSE , lover = %s WHERE  user_id = %s::text", (None,
                                                                                                          str(user_id)))
            cur.execute(
                "UPDATE public.user SET married = FALSE, lover= %s WHERE  user_id = %s::text", (None, str(lover_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()
