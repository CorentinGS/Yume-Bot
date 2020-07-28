import psycopg2
from psycopg2 import extras

from modules.sql.guild import Guild
from modules.sql.user import User

try:
    con = psycopg2.connect("host=postgre dbname=yumebot port=5432 user=postgres password=yumebot")
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
except psycopg2.DatabaseError as e:
    print('Error %s' % e)


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
        try:
            cur.execute("SELECT * FROM public.chan_network WHERE chan_id = {};".format(chan_id))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            return True
        return False

    @staticmethod
    def get_linked_from_guild(guild_id: int):
        try:
            cur.execute("SELECT * FROM public.chan_network WHERE guild_id = {};".format(guild_id))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            return rows
        return {}

    @staticmethod
    def get_all_linked_channels():
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
        try:
            cur.execute(
                "INSERT INTO public.rankings ( guild_id, chan_id)  VALUES ( {}, {});".format(
                    guild_id, chan_id))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def delete_channel(chan_id: int):
        try:
            cur.execute(
                "DELETE FROM public.chan_network WHERE chan_id = {};".format(
                    chan_id))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()
