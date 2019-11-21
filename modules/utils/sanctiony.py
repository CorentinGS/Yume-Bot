#  Copyright (c) 2019.
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
import datetime

from modules.utils.db import Settings


class SanctionY:
    def __init__(self, id: str):
        # Bad guy
        self.user: str = " "
        self.user_id: str = "0"

        # Event
        self.event: str = " "
        self.reason: str = " "
        self.time: str = "0"
        self.date = datetime.datetime.now()
        self.id = id

        # Mod
        self.mod: str = " "
        self.mod_id: str = "0"

        # Guild
        self.guild: str = " "
        self.guild_id: str = "0"

    async def set(self):

        set = await Settings().get_sanction_settings(self.id)

        set['user'] = self.user
        set['user_id'] = self.user_id

        set['moderator'] = self.mod
        set['moderator_id'] = self.mod_id

        set['guild'] = self.guild
        set['guild_id'] = self.guild_id

        set['event'] = self.event
        set['reason'] = self.reason
        set['time'] = self.time
        set['date'] = self.date

        await Settings().set_sanction_settings(self.id, set)

    async def get(self):
        set = await Settings().get_sanction_settings(self.id)
        if not set:
            return False
        else:
            self.user = set["user"]
            self.user_id = set['user_id']
    
            self.mod = set["moderator"]
            self.mod_id = set["moderator_id"]
    
            self.guild = set['guild']
            self.guild_id = set['guild_id']
    
            self.event = set['event']
            self.reason = set['reason']
            self.time = set['time']
            self.date = set['date']
            return True
