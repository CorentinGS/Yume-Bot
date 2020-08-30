import psycopg2

from modules.sql.dbConnect import Db

try:
    con = psycopg2.connect("host=postgre dbname=yumebot port=5432 user=postgres password=yumebot")
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
except psycopg2.DatabaseError as e:
    print('Error %s' % e)


class AnonDB:

    @staticmethod
    def rows_to_dict(rows) -> dict:
        anon = {"channel_id": rows[0], "guild_id": rows[1]}
        return anon

    @staticmethod
    def get_channel(guild_id: int):
        con, meta = Db.connect()
        t_anon = meta.tables['anon']
        try:
            clause = t_anon.select().where(t_anon.c.guild_id == str(guild_id))
            rows = con.execute(clause)
            row = rows.fetchone()
            if row:
                return AnonDB.rows_to_dict(row)
            return None
        except Exception as err:
            print(err)

    @staticmethod
    def set_channel(guild_id: int, channel_id: int):
        if AnonDB.is_setup(guild_id):
            try:
                cur.execute("UPDATE public.anon SET channel_id = {} WHERE guild_id = {}".format(channel_id, guild_id))
            except Exception as err:
                print(err)
                con.rollback()
            con.commit()
        else:
            try:
                cur.execute(
                    "INSERT INTO public.anon (guild_id, channel_id)  "
                    "VALUES ( %s, %s);", (
                        guild_id, channel_id))
            except Exception as err:
                print(err)
                con.rollback()
            con.commit()

    @staticmethod
    def unset_channel(guild_id: int):
        try:
            cur.execute("DELETE FROM public.anon WHERE guild_id = {};".format(guild_id))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def is_setup(guild_id: int):
        try:
            cur.execute("SELECT * FROM public.anon WHERE guild_id = {};".format(guild_id))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            return True
        return False

    @staticmethod
    def is_blocked(user_id: int, guild_id: int):
        try:
            cur.execute(
                "SELECT * FROM public.anon_users WHERE guild_id = {} AND user_id = {};".format(guild_id, user_id))
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
        try:
            cur.execute("INSERT INTO public.anon_users ( user_id, guild_id) VALUES ( %s, %s );", (user_id, guild_id))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def is_author(user_id: int, guild_id: int):
        try:
            cur.execute(
                "SELECT * FROM public.anon_users WHERE guild_id = {} AND user_id = {};".format(guild_id, user_id))
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
        try:
            cur.execute("SELECT * FROM public.anon_logs WHERE message_id = {};".format(message_id))
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
        try:
            cur.execute(
                "INSERT INTO public.anon_logs ( message_id, guild_id, user_id) VALUES ( %s, %s, %s );",
                (message_id, guild_id, user_id))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def block_anon(user_id: int, guild_id: int):
        try:
            cur.execute(
                "UPDATE public.anon_users SET blocked = true WHERE user_id = {} AND guild_id = {};".format(user_id,
                                                                                                           guild_id))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()

    @staticmethod
    def unblock_anon(user_id: int, guild_id: int):
        try:
            cur.execute(
                "UPDATE public.anon_users SET blocked = false WHERE user_id = {} AND guild_id = {};".format(user_id,
                                                                                                            guild_id))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()
