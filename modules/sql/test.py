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

import asyncpg
import psycopg2
from psycopg2 import extras

from modules.sql.user import User


class TestDB:

    @staticmethod
    def user_from_row(rows):
        return User(rows['user_id'], rows['vip'], rows['crew'], rows['description'])

    @staticmethod
    def users_from_row(rows):
        users = []
        for row in rows:
            users.append(TestDB.user_from_row(row))
        return users

    """
    Get methods
    """

    @staticmethod
    async def get_one(db, user_id: int) -> User:
        rows = await db.fetchrow("SELECT * FROM public.user WHERE user_id = {};".format(user_id))
        if rows:
            return TestDB.user_from_row(rows)

    @staticmethod
    async def get_all(db: asyncpg.pool.Pool) -> list:
        rows = await db.fetch("SELECT * FROM public.user;")
        if rows:
            return TestDB.users_from_row(rows)

    @staticmethod
    async def update_user(db: asyncpg.pool.Pool, user: User):
        connection = await db.acquire()
        async with connection.transaction():
            await db.execute(
                "UPDATE public.user SET description = '{}', crew = '{}', vip = '{}' WHERE  user_id = {}".format(
                    str(user.description), user.crew, user.vip, user.user_id))
        await db.release(connection)


async def run():
    db = await asyncpg.create_pool(user="postgres", host="localhost", port="5432", database="yumebot")

    x = await TestDB.get_one(db, 282233191916634113)
    x.display()
    y = await TestDB.get_all(db)
    print(y)
    x.description = "Toto"
    await TestDB.update_user(db, x)
    u = await TestDB.get_one(db, 282233191916634113)
    u.display()


# loop = asyncio.get_event_loop()
# loop.run_until_complete(run())


con = psycopg2.connect("host=localhost dbname=yumebot port=5432 user=postgres")
cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)

cur.execute("SELECT * FROM public.blacklist")
print(cur.fetchone())
