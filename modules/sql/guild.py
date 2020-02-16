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

class Guild:
    def __init__(self, guild_id: int, blacklist: bool = False, color: bool = False, greet: bool = False,
                 greet_chan: int = 0, log_chan: int = 0, logging: bool = False, setup: bool = False,
                 stats_category: int = 0, stats_channels: bool = False, vip: bool = False):
        self.guild_id = guild_id
        self.blacklist = blacklist
        self.color = color
        self.greet = greet
        self.greet_chan = greet_chan
        self.log_chan = log_chan
        self.logging = logging
        self.setup = setup
        self.stats_category = stats_category
        self.stats_channels = stats_channels
        self.vip = vip

    def display(self):
        print("GuildID : {}".format(self.guild_id))
        print("Is Vip : {}".format(self.vip))
        print("Is Setup : {}".format(self.setup))