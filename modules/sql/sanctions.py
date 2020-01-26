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

import datetime


class Sanction:
    def __init__(self, sanction_id: int, event: str = "", guild_id: int = 0, moderator_id: int = 0, reason: str = 0,
                 time: int = 0, user_id: int = 0, event_date: datetime.datetime = datetime.datetime.now()):
        self.event = event
        self.guild_id = guild_id
        self.moderator_id = moderator_id
        self.reason = reason
        self.sanction_id = sanction_id
        self.time = time
        self.user_id = user_id
        self.event_date = event_date

    def display(self):
        print("UserID : {}".format(self.user_id))
        print("Event : {}".format(self.event))
        print("ModeratorID : {}".format(self.moderator_id))
        print("Reason : {}".format(self.reason))
