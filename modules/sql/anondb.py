import psycopg2

from modules.sql.dbConnect import Db


class AnonDB:

    @staticmethod
    def rows_to_dict(rows) -> dict:
        anon = {"channel_id": rows[0], "guild_id": rows[1]}
        return anon

    @staticmethod
    def get_channel(guild_id: int):
        con, cur = Db.connect()
        try:
            cur.execute("SELECT * FROM public.anon WHERE guild_id = {}::text;".format(str(guild_id)))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            return AnonDB.rows_to_dict(rows)
        return None

    @staticmethod
    def set_channel(guild_id: int, channel_id: int):
        con, cur = Db.connect()

        if AnonDB.is_setup(guild_id):
            try:
                cur.execute(
                    "UPDATE public.anon SET channel_id = {}::text WHERE guild_id = {}::text".format(str(channel_id),
                                                                                                    str(guild_id)))
            except Exception as err:
                print(err)
                con.rollback()
            con.commit()
        else:
            try:
                cur.execute(
                    "INSERT INTO public.anon (guild_id, channel_id)  "
                    "VALUES ( %s::text, %s::text);", (
                        str(guild_id), str(channel_id)))
            except Exception as err:
                print(err)
                con.rollback()
            con.commit()

    @staticmethod
    def unset_channel(guild_id: int):
        con, cur = Db.connect()

        try:
            cur.execute("DELETE FROM public.anon WHERE guild_id = {}::text;".format(str(guild_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def is_setup(guild_id: int):
        con, cur = Db.connect()

        try:
            cur.execute("SELECT * FROM public.anon WHERE guild_id = {}::text;".format(str(guild_id)))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            return True
        return False

    @staticmethod
    def is_blocked(user_id: int, guild_id: int):
        con, cur = Db.connect()

        try:
            cur.execute(
                "SELECT * FROM public.anon_users WHERE guild_id = {}::text AND user_id = {}::text;".format(
                    str(guild_id),
                    str(user_id)))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            if rows['blocked'] is True:
                return True
            else:
                return False

    @staticmethod
    def set_author(user_id: int, guild_id: int):
        con, cur = Db.connect()

        try:
            cur.execute("INSERT INTO public.anon_users ( user_id, guild_id) VALUES ( %s::text, %s::text );",
                        (str(user_id), str(guild_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def is_author(user_id: int, guild_id: int):
        con, cur = Db.connect()

        try:
            cur.execute(
                "SELECT * FROM public.anon_users WHERE guild_id = {}::text AND user_id = {}::text;".format(
                    str(guild_id),
                    str(user_id)))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            return True
        else:
            return False

    @staticmethod
    def get_message(message_id: int):
        con, cur = Db.connect()

        try:
            cur.execute("SELECT * FROM public.anon_logs WHERE message_id = {}::text;".format(str(message_id)))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            message = {"user_id": rows["user_id"],
                       "message_id": rows["message_id"],
                       "guild_id": rows["guild_id"]
                       }
            return message
        else:
            return {}

    @staticmethod
    def set_message(message_id: int, user_id: int, guild_id: int):
        con, cur = Db.connect()

        try:
            cur.execute(
                "INSERT INTO public.anon_logs ( message_id, guild_id, user_id) VALUES ( %s::text, %s::text, %s::text );",
                (str(message_id), str(guild_id), str(user_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def block_anon(user_id: int, guild_id: int):
        con, cur = Db.connect()

        try:
            cur.execute(
                "UPDATE public.anon_users SET blocked = true WHERE user_id = {}::text AND guild_id = {}::text;".format(str(user_id),
                                                                                                           str(
                                                                                                               guild_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def unblock_anon(user_id: int, guild_id: int):
        con, cur = Db.connect()

        try:
            cur.execute(
                "UPDATE public.anon_users SET blocked = false WHERE user_id = {}::text AND guild_id = {}::text;".format(
                    str(user_id),
                    str(guild_id)))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()
