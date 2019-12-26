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
import motor.motor_asyncio


class Settings:

    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient('mongo', 27017)

        self.db = self.client.bot

        self.servers = self.db.servers

        self.glob = self.db.glob
        self.keys = self.db.keys
        self.sanction = self.db.sanction
        self.user = self.db.user
        self.reaction = self.db.reaction
        self.custom = self.db.custom

    async def get_glob_settings(self):
        doc = await self.glob.find_one({"_id": 0})
        return doc or {}

    async def set_glob_settings(self, settings):
        return await self.glob.replace_one({"_id": 0}, settings, True)

    async def set_server_settings(self, id, settings):
        return await self.servers.replace_one({"_id": id}, settings, True)

    async def get_server_settings(self, id):
        doc = await self.servers.find_one({"_id": id})
        return doc or {}

    async def get_all_server_settings(self):
        doc = await self.servers.find()
        return doc or {}

    async def del_server_settings(self, id):
        await self.servers.remove({"_id": id})

    async def get_reaction_settings(self, id):
        doc = await self.reaction.find_one({"_id": id})
        return doc or {}

    async def del_reaction_settings(self, id):
        await self.reaction.remove({"_id": id})

    async def set_reaction_settings(self, id, settings):
        return await self.reaction.replace_one({"_id": id}, settings, True)

    async def set_custom_settings(self, id, settings):
        return await self.custom.replace_one({"_id": id}, settings, True)

    async def get_custom_settings(self, id):
        doc = await self.custom.find_one({"_id": id})
        return doc or {}

    async def get_user_settings(self, id):
        doc = await self.user.find_one({"_id": id})
        return doc or {}

    async def set_user_settings(self, id, settings):
        return await self.user.replace_one({"_id": id}, settings, True)

    async def get_key_settings(self, name):
        doc = await self.keys.find_one({"_id": name})
        return doc or {}

    async def set_key_settings(self, name, settings):
        return await self.keys.replace_one({"_id": name}, settings, True)

    async def get_sanction_settings(self, id):
        doc = await self.sanction.find_one({"_id": id})
        return doc or {}

    async def set_sanction_settings(self, id, settings):
        return await self.sanction.replace_one({"_id": id}, settings, True)

    async def get_sanction_settings_member(self, user, guild):
        doc = []
        async for docu in self.sanction.find({"user_id": user, "guild_id": guild}):
            doc.append(docu['_id'])
        return doc or {}

    async def get_sanction_settings_user(self, user):
        doc = []
        async for docu in self.sanction.find({"user_id": user}):
            doc.append(docu['_id'])
        return doc or {}

    async def rm_strike_settings(self, guild, user):
        return await self.sanction.delete_many({"guild_id": guild, "user_id": user})
