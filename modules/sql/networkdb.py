import psycopg2
from psycopg2 import extras

from modules.sql.dbConnect import Db


class NetworkDB:

    @staticmethod
    def row_to_dict(rows) -> dict:
        channel = {"chan": rows['chan_id'], "guild": rows['guild_id']}
        return channel

    @staticmethod
    def channels_from_rows(rows) -> list:
        channels = []
        for row in rows:
            channels.append(NetworkDB.row_to_dict(row))
        return channels

    """
    Get methods
    """

    @staticmethod
    def is_linked(chan_id: int):
        con, cur = Db.connect()

        try:
            cur.execute("SELECT * FROM public.chan_network WHERE chan_id = {}::text;".format(str(chan_id)))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            return True
        return False

    @staticmethod
    def get_linked_from_guild(guild_id: int):
        con, cur = Db.connect()

        try:
            cur.execute("SELECT * FROM public.chan_network WHERE guild_id = {}::text;".format(str(guild_id)))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            return rows
        return {}

    @staticmethod
    def get_all_linked_channels():
        con, cur = Db.connect()

        try:
            cur.execute("SELECT * FROM public.chan_network;")
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchall()
        if rows:
            channels: list = NetworkDB.channels_from_rows(rows)
            return channels
        return []

    """
    Set methods
    """

    @staticmethod
    def set_channel(chan_id: int, guild_id: int):
        con, cur = Db.connect()

        try:
            cur.execute(
                "INSERT INTO public.chan_network ( guild_id, chan_id)  VALUES ( {}::text, {}::text);".format(
                    str(guild_id), str(chan_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def delete_channel(chan_id: int):
        con, cur = Db.connect()

        try:
            cur.execute(
                "DELETE FROM public.chan_network WHERE chan_id = {}::text;".format(
                    str(chan_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def block_user(user_id: int):
        con, cur = Db.connect()

        try:
            cur.execute(
                "INSERT INTO public.user_network ( user_id) VALUES ( {}::text );".format(str(user_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def unblock_user(user_id: int):
        con, cur = Db.connect()

        try:
            cur.execute(
                "DELETE FROM public.user_network WHERE user_id = {}::text;".format(str(user_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def is_blocked(user_id: int):
        con, cur = Db.connect()

        try:
            cur.execute(
                "SELECT * FROM public.user_network WHERE user_id = {}::text;".format(str(user_id)))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchall()
        if rows:
            return True
        return False
