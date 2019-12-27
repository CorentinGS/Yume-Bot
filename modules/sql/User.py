#  Copyright (c) 2019.
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

try:
    con = psycopg2.connect("host=localhost dbname=yumebot user=postgres")
    cur = con.cursor()
except psycopg2.DatabaseError as e:
    print('Error %s' % e)


class Methods:
    @staticmethod
    def get():
        cur.execute("SELECT * FROM public.user;)")
        rows = cur.fetchall()
        if rows:
            return rows
        return "Error: No user"

    @staticmethod
    def get_crew():
        cur.execute("SELECT * FROM public.user WHERE crew = TRUE;)")
        rows = cur.fetchall()
        if rows:
            return rows
        return "Error: No Crew"

    @staticmethod
    def get_vip():
        cur.execute("SELECT * FROM public.user WHERE vip = TRUE")
        rows = cur.fetchall()
        if rows:
            return rows
        return "Error : No VIP"


class User:
    def __init__(self, user_id, crew: bool = False, vip: bool = False, description: str = ""):
        self.user_id: id = user_id
        self.crew: bool = crew
        self.vip: bool = vip
        self.description: str = description

    async def get(self):
        cur.execute("SELECT FROM public.user WHERE user_id = {};".format(self.user_id))
        rows = cur.fetchone()
        if rows:
            return rows
        return "Error : User not found"

    def is_crew(self):
        cur.execute("SELECT crew FROM public.user WHERE user_id = {}".format(self.user_id))
        rows = cur.fetchone()
        if rows:
            return rows[0]
        return False

    def is_vip(self):
        cur.execute("SELECT vip FROM public.user WHERE user_id = {}".format(self.user_id))
        rows = cur.fetchone()
        if rows:
            return rows[0]
        return False

    def user_exists(self):
        cur.execute("SELECT FROM public.user WHERE user_id = {};".format(self.user_id))
        rows = cur.fetchone()
        if rows:
            return True
        return False

    def create(self):
        cur.execute("INSERT INTO public.user ( crew, description, user_id, vip) VALUES ( %s, %s, %s, %s);",
                    (self.crew, self.description, self.user_id, self.vip))
        con.commit()

    def delete(self):
        cur.execute("DELETE FROM public.user WHERE user_id = %s;", self.user_id)
        con.commit()

    def update_desc(self, description: str):
        cur.execute("UPDATE public.user SET description = %s WHERE  user_id = %s", (description, self.user_id))
        cur.commit()

    def set_vip(self):
        cur.execute("UPDATE public.user SET vip = TRUE WHERE  user_id = %s", self.user_id)
        cur.commit()

    def set_crew(self):
        cur.execute("UPDATE public.user SET crew = TRUE WHERE  user_id = %s", self.user_id)
        cur.commit()

    def unset_vip(self):
        cur.execute("UPDATE public.user SET vip = FALSE WHERE  user_id = %s", self.user_id)
        cur.commit()

    def unset_crew(self):
        cur.execute("UPDATE public.user SET crew = FALSE WHERE  user_id = %s", self.user_id)
        cur.commit()


toto = User(282233191916634113).is_crew()

patate = User(294897996837945344)
print(patate.user_exists())

if patate.user_exists():
    print(patate.get())

print(toto)
