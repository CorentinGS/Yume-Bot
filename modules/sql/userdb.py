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
        return User(rows[0], rows[1], rows[2], rows[3], rows[4], rows[5])

    """
    Get methods
    """

    @staticmethod
    def get_one(user_id: int) -> User:
        con, meta = Db.connect()
        t_user = meta.tables['user']
        try:
            clause = t_user.select().where(t_user.c.user_id == str(user_id))
            rows = con.execute(clause)
            row = rows.fetchone()
            if row:
                return UserDB.user_from_row(row)
            else:
                u = User(user_id)
                UserDB.create(u)
                return u
        except Exception as err:
            print(err)

    @staticmethod
    def get_vips():
        con, meta = Db.connect()
        t_user = meta.tables['user']
        users = []
        try:
            clause = t_user.select().where(t_user.c.vip == True)
            for rows in con.execute(clause):
                for row in rows:
                    users.append(UserDB.user_from_row(row))
                return users
        except Exception as err:
            print(err)

    """
    Checks methods
    """

    @staticmethod
    def is_vip(user: User) -> bool:
        con, meta = Db.connect()
        t_user = meta.tables['user']
        try:
            clause = t_user.select(t_user.c.vip).where(t_user.c.user_id == str(user.user_id))
            rows = con.execute(clause)
            if rows:
                return rows[0]
            return False
        except Exception as err:
            print(err)

    """
    Create & delete methods
    """

    @staticmethod
    def create(user: User):
        con, meta = Db.connect()
        t_user = meta.tables['user']
        try:
            clause = t_user.insert().values(
                crew=user.crew,
                description=user.description,
                user_id=user.user_id,
                vip=user.vip
            )
            con.execute(clause)
        except Exception as err:
            print(err)

    """
    Set methods
    """

    @staticmethod
    def set_vip(user: User):
        con, meta = Db.connect()
        t_user = meta.tables['user']
        try:
            clause = t_user.update().where(t_user.c.user_id == str(user.user_id)).values(
                vip=user.vip
            )
            con.execute(clause)
        except Exception as err:
            print(err)

    @staticmethod
    def set_lover(user_id: int, lover_id: int):
        con, meta = Db.connect()
        t_user = meta.tables['user']
        try:
            clause = t_user.update().where(t_user.c.user_id == str(user_id)).values(
                married=True,
                lover=lover_id
            )
            con.execute(clause)
        except Exception as err:
            print(err)
        try:
            clause = t_user.update().where(t_user.c.user_id == str(lover_id)).values(
                married=True,
                lover=user_id
            )
            con.execute(clause)
        except Exception as err:
            print(err)

    """
    Unset methods
    """

    @staticmethod
    def unset_vip(user: User):
        con, meta = Db.connect()
        t_user = meta.tables['user']
        try:
            clause = t_user.update().where(t_user.c.user_id == str(user.user_id)).values(
                vip=False,
            )
            con.execute(clause)
        except Exception as err:
            print(err)

    @staticmethod
    def unset_lover(user: User, lover: User):
        con, meta = Db.connect()
        t_user = meta.tables['user']
        try:
            clause = t_user.update().where(t_user.c.user_id == str(user.user_id)).values(
                married=False,
                lover=None
            )
            con.execute(clause)
        except Exception as err:
            print(err)
        try:
            clause = t_user.update().where(t_user.c.user_id == str(lover.user_id)).values(
                married=False,
                lover=None
            )
            con.execute(clause)
        except Exception as err:
            print(err)
