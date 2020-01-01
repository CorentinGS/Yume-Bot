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

#
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#
#
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#
#
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#
import psycopg2
import pymongo

client = pymongo.MongoClient('localhost', 27018)
con = psycopg2.connect("host=localhost dbname=yumebot user=postgres")

cur = con.cursor()

db = client.bot
collection_server = db.servers
collection_sanction = db.sanction
collection_rankings = db.user

servers = collection_server.find()

for sanction in collection_sanction.find():
    cur.execute("INSERT INTO public.sanctions ( event_date, event, guild, guild_id, moderator, moderator_id, reason, sanction_id, time, user_id) \
        VALUES (  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );", (
        sanction['date'], sanction['event'], sanction['guild'], sanction['guild_id'], sanction['moderator'],
        sanction['moderator_id'], sanction['reason'], sanction['_id'], sanction['time'],
        sanction['user_id']))

for server in servers:
    cur.execute("INSERT INTO public.guild ( blacklist, color, greet, greetchan, guild_id, log_chan, logging, setup, stats_category, stats_channels, vip) \
    VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", (server['bl'], server['Color'], server['Greet'],
                                                             server['GreetChannel'], server['_id'],
                                                             server['LogChannel'], server['logging'], server['Setup'],
                                                             server['category'],
                                                             server['Display'], server['Vip']))

    for user in server['Admins']:
        cur.execute("INSERT INTO public.admin ( admin, guild_id, user_id) VALUES ( %s, %s, %s);",
                    (True, server['_id'], user))
    for user in server['Mods']:
        cur.execute("INSERT INTO public.admin ( admin, guild_id, user_id) VALUES ( %s, %s, %s);",
                    (False, server['_id'], user))
    if 'levels' in server:
        for level in server['levels']:
            cur.execute("INSERT INTO public.roles ( guild_id, level, role_id) VALUES ( %s, %s, %s );",
                        (server['_id'], level, server['levels'][level]))

for guild in collection_rankings.find():
    for user in guild:
        if isinstance(guild[user], str):
            continue

        cur.execute(
            "INSERT INTO public.rankings ( guild_id, level, reach, total, user_id, xp) VALUES ( %s, %s, %s, %s, %s, %s );",
            (guild['_id'], guild[user]['level'], guild[user]['reach'], guild[user]['total'], user, guild[user]['xp']))

con.commit()
