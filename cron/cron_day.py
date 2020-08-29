import json
from datetime import datetime, timedelta

import psycopg2
from psycopg2 import extras

with open("./config/keys.json", "r") as cjson:
    keys = json.load(cjson)


def connect():
    try:
        con = psycopg2.connect(
            "host=localhost dbname=yumebot port=5432 user=postgres password={}".format(keys["postgresql"]))
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    except psycopg2.DatabaseError as e:
        print('Error %s' % e)

    return con, cur


def delete(con, cur, last_week_formatted):
    try:
        cur.execute('DELETE FROM public.messages WHERE time_id = {}'.format(last_week_formatted))
    except Exception as err:
        print(err)
        con.rollback()
    con.commit()


def message_rotate(con, cur, last_week_formatted):
    try:
        cur.execute('INSERT INTO public.daily_messages ( guild_id, date_id, counter) SELECT public.messages.guild_id ,'
                    'public.messages.time_id , count(*) FROM public.messages WHERE time_id = {}'
                    'GROUP BY public.messages.guild_id, public.messages.time_id '
                    'ORDER BY public.messages.guild_id ASC, public.messages.time_id;'.format(last_week_formatted))
    except Exception as err:
        print(err)
        con.rollback()
    con.commit()


def main():
    print("main")
    date = datetime.today()
    last_week = date - timedelta(days=7)
    last_week_formatted = last_week.strftime("%Y%m%d")
    con, cur = connect()
    try:
        cur.execute('SELECT count(*) FROM public.messages WHERE time_id = {}'.format(last_week_formatted))
    except Exception as err:
        print(err)
        con.rollback()
    result = cur.fetchone()
    print("Rotate {} messages".format(result))
    message_rotate(con, cur, last_week_formatted)
    delete(con, cur, last_week_formatted)


main()
