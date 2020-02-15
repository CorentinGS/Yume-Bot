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

from modules.sql.guild import Guild
from modules.sql.user import User

try:
    con = psycopg2.connect("host=postgre dbname=yumebot port=5432 user=postgres")
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
except psycopg2.DatabaseError as e:
    print('Error %s' % e)


class UserDB:

    @staticmethod
    def user_from_row(rows):
        return User(rows['user_id'], rows['vip'], rows['crew'], rows['description'])

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
        try:
            cur.execute("SELECT * FROM public.user WHERE user_id = {};".format(user_id))
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
    def get_user(user: User) -> User:
        try:
            cur.execute("SELECT * FROM public.user WHERE user_id = {};".format(user.user_id))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            return UserDB.user_from_row(rows)
        else:
            UserDB.create(user)
            return user

    @staticmethod
    def get_all() -> list:
        try:
            cur.execute("SELECT * FROM public.user;")
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchall()
        if rows:
            return UserDB.users_from_row(rows)
        return []

    @staticmethod
    def get_crews():
        try:
            cur.execute("SELECT * FROM public.user WHERE crew = TRUE;")
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchall()
        if rows:
            return UserDB.users_from_row(rows)
        return "Error: No Crew"

    @staticmethod
    def get_vips():
        try:
            cur.execute("SELECT * FROM public.user WHERE vip = TRUE")
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchall()
        if rows:
            return UserDB.users_from_row(rows)
        return "Error : No VIP"

    """
    Checks methods
    """

    @staticmethod
    def is_crew(user: User) -> bool:
        try:
            cur.execute("SELECT crew FROM public.user WHERE user_id = {}".format(user.user_id))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            return rows[0]
        return False

    @staticmethod
    def is_vip(user: User) -> bool:
        try:
            cur.execute("SELECT vip FROM public.user WHERE user_id = {}".format(user.user_id))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            return rows[0]
        return False

    @staticmethod
    def user_exists(user: User) -> bool:
        try:
            cur.execute("SELECT count(*) FROM public.user WHERE user_id = {};".format(user.user_id))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows[0] > 0:
            return True
        return False

    """
    Create & delete methods
    """

    @staticmethod
    def create(user: User):
        try:
            cur.execute("INSERT INTO public.user ( crew, description, user_id, vip) VALUES ( %s, %s, %s, %s);",
                        (user.crew, user.description, user.user_id, user.vip))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def delete(user: User):
        try:
            cur.execute("DELETE FROM public.user WHERE user_id = {};".format(user.user_id))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    """
    Update methods
    """

    @staticmethod
    def update_desc(user: User, description: str):
        try:
            cur.execute(
                "UPDATE public.user SET description = '{}' WHERE  user_id = {}".format(str(description), user.user_id))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def update_user(user: User):
        try:
            cur.execute("UPDATE public.user SET description = '{}', crew = '{}', vip = '{}' WHERE  user_id = {}".format(
                str(user.description), user.crew, user.vip, user.user_id))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    """
    Set methods
    """

    @staticmethod
    def set_vip(user: User):
        try:
            cur.execute("UPDATE public.user SET vip = TRUE WHERE  user_id = {}".format(user.user_id))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def set_crew(user: User):
        try:
            cur.execute("UPDATE public.user SET crew = TRUE WHERE  user_id = {}".format(user.user_id))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    """
    Unset methods
    """

    @staticmethod
    def unset_vip(user: User):
        try:
            cur.execute("UPDATE public.user SET vip = FALSE WHERE  user_id = {}".format(user.user_id))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def unset_crew(user: User):
        try:
            cur.execute("UPDATE public.user SET crew = FALSE WHERE  user_id = {}".format(user.user_id))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    """
    Others Methods
    """

    @staticmethod
    def is_muted(guild: Guild, user: User) -> bool:
        try:
            cur.execute(
                "SELECT * FROM public.muted WHERE guild_id = {} AND user_id = {}".format(guild.guild_id, user.user_id))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            return True
        return False
