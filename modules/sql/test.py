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

from modules.sql.guild import Guild
from modules.sql.rankingsdb import RankingsDB
from modules.sql.sanctionsdb import SanctionsDB
from modules.sql.user import User
from modules.sql.userdb import UserDB

titi: User = User(443882750559387668, True, False, "Hello world")
if UserDB.user_exists(titi):
    UserDB.delete(titi)
UserDB.create(titi)

roles = [661873465556598784, 631811831559880724, 661880943791046680]
'''
Is AFK

afk, row = UserDB.is_afk(titi)
print(row[2])
if afk:
    print("This user is afk for the reason : {} for {} minutes".format(row[1], (datetime.now(timezone('UTC')) - row[2]).total_seconds() // 60.0))
'''

tux: Guild = Guild(631811291568144384)


tux.display()
if not RankingsDB.ranking_exists(titi, tux):
    RankingsDB.create_ranking(titi, tux)
else:
    print("EXISTS")

rankings = RankingsDB.get_user(titi, tux)
rankings['xp'] += 15
RankingsDB.update_user(titi, tux, rankings)

print(RankingsDB.get_rank(titi, tux))
'''
Get Admin roles 

toto = GuildDB.get_admin_roles(tux)
print(toto)
print(list(set(toto).intersection(roles)))
'''

patate = SanctionsDB.get_sanctions_from_user(titi)
for sanction in patate:
    print(sanction.sanction_id)

print(RankingsDB.get_scoreboard(tux))