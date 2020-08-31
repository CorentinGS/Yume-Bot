import psycopg2
from psycopg2 import extras

from modules.sql.dbConnect import Db


class PrivateDB:

    @staticmethod
    def rows_to_dict(rows) -> dict:
        private = {"cat_id": rows['cat_id'], "guild_id": rows['guild_id'], "name_prefix": rows['name_prefix'],
                   "role_id": rows['role_id'], "hub_id": rows['hub_id']}
        return private

    @staticmethod
    def get_one(guild_id: int, cat_id: int) -> dict:
        con, cur = Db.connect()

        try:
            cur.execute(
                "SELECT * FROM public.private WHERE cat_id = {}::text and guild_id = {}::text;".format(str(cat_id),
                                                                                                       str(guild_id)))
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
        con, cur = Db.connect()

        try:
            cur.execute(
                "INSERT INTO public.private ( cat_id, guild_id, role_id, hub_id, name_prefix)  "
                "VALUES ( %s::text, %s::text, %s::text, %s::text, %s);", (
                    str(private['cat_id']), str(private['guild_id']), str(private['role_id']),
                    str(private['hub_id']), private['name_prefix']))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def delete_one(guild_id: int, cat_id: int):
        con, cur = Db.connect()

        try:
            cur.execute(
                "DELETE FROM public.private WHERE guild_id = {}::text and cat_id = {}::text;".format(str(guild_id),
                                                                                                     str(cat_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def create_user_one(user_id: int, cat_id: int, chan_id: int):
        con, cur = Db.connect()

        try:
            cur.execute(
                "INSERT INTO public.private_users ( cat_id, user_id, chan_id)  VALUES ( {}::text, {}::text, {}::text);".format(
                    str(cat_id), str(user_id), str(chan_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def has_channel(user_id: int, cat_id: int):
        con, cur = Db.connect()

        try:
            cur.execute(
                "SELECT * FROM public.private_users WHERE user_id = {}::text and cat_id = {}::text;".format(
                    str(user_id),
                    str(cat_id)))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            return True
        return False

    @staticmethod
    def get_user(user_id: int, cat_id: int):
        con, cur = Db.connect()

        try:
            cur.execute(
                "SELECT * FROM public.private_users WHERE user_id = {}::text and cat_id = {}::text;".format(
                    str(user_id),
                    str(cat_id)))
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
        con, cur = Db.connect()

        try:
            cur.execute(
                "DELETE FROM public.private_users WHERE user_id = {}::text and cat_id = {}::text;".format(str(user_id),
                                                                                                          str(cat_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()
