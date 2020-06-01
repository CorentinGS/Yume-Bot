import psycopg2
from psycopg2 import extras

try:
    con = psycopg2.connect("host=postgre dbname=yumebot port=5432 user=postgres password=yumebot")
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
except psycopg2.DatabaseError as e:
    print('Error %s' % e)


class PrivateDB:

    @staticmethod
    def rows_to_dict(rows) -> dict:
        private = {"cat_id": rows['cat_id'], "guild_id": rows['guild_id'], "name_prefix": rows['name_prefix'],
                   "role_id": rows['role_id'], "hub_id": rows['hub_id']}
        return private

    @staticmethod
    def get_one(guild_id: int, cat_id: int) -> dict:
        try:
            cur.execute("SELECT * FROM public.private WHERE cat_id = {} and guild_id = {};".format(cat_id, guild_id))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            private = PrivateDB.rows_to_dict(rows)
            return private
        return {}

    @staticmethod
    def create_one(private: dict):
        try:
            cur.execute(
                "INSERT INTO public.private ( cat_id, guild_id, role_id, hub_id, name_prefix)  "
                "VALUES ( %s, %s, %s, %s, %s);", (
                    private['cat_id'], private['guild_id'], private['role_id'],
                    private['hub_id'], private['name_prefix']))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def delete_one(guild_id: int, cat_id: int):
        try:
            cur.execute(
                "DELETE FROM public.private WHERE guild_id = {} and cat_id = {};".format(guild_id, cat_id))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def create_user_one(user_id: int, cat_id: int, chan_id: int):
        print(chan_id)
        try:
            cur.execute(
                "INSERT INTO public.private_users ( cat_id, user_id, chan_id)  VALUES ( {}, {}, {});".format(
                    cat_id, user_id, chan_id))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def has_channel(user_id: int, cat_id: int):
        try:
            cur.execute(
                "SELECT * FROM public.private_users WHERE user_id = {} and cat_id = {};".format(user_id, cat_id))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            return True
        return False

    @staticmethod
    def get_user(user_id: int, cat_id: int):
        try:
            cur.execute(
                "SELECT * FROM public.private_users WHERE user_id = {} and cat_id = {};".format(user_id, cat_id))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            users = {"user_id": rows["user_id"],
                     "cat_id": rows["cat_id"],
                     "chan_id": rows["chan_id"]
                     }

            return users
        return {}

    @staticmethod
    def delete_user(user_id: int, cat_id: int):
        try:
            cur.execute(
                "DELETE FROM public.private_users WHERE user_id = {} and cat_id = {};".format(user_id, cat_id))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()
