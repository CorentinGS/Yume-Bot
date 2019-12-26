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
import discord

from modules.utils.db import Settings


class GuildY:

    def __init__(self, guild: discord.Guild):
        # Settings
        self.automod: bool = False
        self.logging: bool = False
        self.greet: bool = False
        self.members_count: bool = False
        self.bl: bool = False
        self.color: bool = False

        # Status
        self.setup: bool = False
        self.vip: bool = False

        # Channels
        self.log_channel: str = "0"
        self.greet_channel: str = "0"
        self.count_category: str = "0"

        # Guild
        self.name = guild.name
        self.id = guild.id

        # Lists
        self.mods = []
        self.admins = []
        self.mute = []
        self.colors = {}

    async def set(self):
        set = await Settings().get_server_settings(str(self.id))

        # Settings
        set['Greet'] = self.greet
        set['bl'] = self.bl
        set['logging'] = self.logging
        set['automod'] = self.automod
        set['Display'] = self.members_count
        set['Color'] = self.color


        # Channels
        set['category'] = self.count_category
        set['GreetChannel'] = self.greet_channel
        set['LogChannel'] = self.log_channel

        # Lists
        set['Admins'] = self.admins
        set['Mods'] = self.mods
        set['Mute'] = self.mute

        # Status
        set['Setup'] = self.setup
        set['Vip'] = self.vip
        set['Colors'] = self.colors

        await Settings().set_server_settings(str(self.id), set)

    async def get(self):
        set = await Settings().get_server_settings(str(self.id))

        # Settings
        self.automod = set["automod"]
        self.logging = set["logging"]
        self.greet = set['Greet']
        self.members_count = set['Display']
        self.bl = set['bl']
        self.color = set['Color']


        # Status
        self.setup = set['Setup']
        self.vip = set["Vip"]

        # Channels
        self.log_channel = set['LogChannel']
        self.greet_channel = set['GreetChannel']
        self.count_category = set["category"]

        # Lists
        self.mods = set['Mods']
        self.admins = set['Admins']
        self.mute = set['Mute']
        self.colors = set['Colors']


class Setup:

    @staticmethod
    async def new_guild(guild_id: int):
        set = await Settings().get_server_settings(str(guild_id))

        set['Greet'] = False
        set['bl'] = False
        set['logging'] = False
        set['GreetChannel'] = None
        set['LogChannel'] = None
        set['automod'] = False
        set['Mute'] = []
        set['Display'] = False
        set['category'] = None
        set['Admins'] = []
        set['Mods'] = []
        set['Setup'] = False
        set['Colors'] = {}
        set['Color'] = False

        await Settings().set_server_settings(str(guild_id), set)

        return True

    @staticmethod
    async def refresh(guild_id: int):
        set = await Settings().get_server_settings(str(guild_id))

        if 'Colors' not in set:
            set['Colors'] = {}
        if 'Color' not in set:
            set['Color'] = False

        await Settings().set_server_settings(str(guild_id), set)

# TODO: Déplacer les objets ici
