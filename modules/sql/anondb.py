import psycopg2

try:
    con = psycopg2.connect("host=postgre dbname=yumebot port=5432 user=postgres password=yumebot")
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
except psycopg2.DatabaseError as e:
    print('Error %s' % e)


class AnonDB:

    @staticmethod
    def rows_to_dict(rows) -> dict:
        anon = {"guild_id": rows['guild_id'], "channel_id": rows['channel_id']}
        return anon

    @staticmethod
    def get_channel(guild_id: int):
        try:
            cur.execute("SELECT * FROM public.anon WHERE guild_id = {};".format(guild_id))
        except Exception as err:
            print(err)
            con.rollback()
        rows = cur.fetchone()
        if rows:
            return AnonDB.rows_to_dict(rows)
        return None

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
