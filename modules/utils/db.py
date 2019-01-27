import motor.motor_asyncio


class Settings():

    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient('mongo', 27017)

        self.db = self.client.bot

        self.glob = self.db.glob
        self.servers = self.db.servers
        self.profiles = self.db.profiles
        self.clans = self.db.clans
        self.keys = self.db.keys
        self.sanction = self.db.sanction

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

    async def get_user_settings(self, id):
        doc = await self.profiles.find_one({"_id": id})
        return doc or {}

    async def set_user_settings(self, id, settings):
        return await self.profiles.replace_one({"_id": id}, settings, True)

    async def get_clan_settings(self, name):
        doc = await self.clans.find_one({"_id": name})
        return doc or {}

    async def set_clan_settings(self, name, settings):
        return await self.clans.replace_one({"_id": name}, settings, True)

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

    async def get_strike_settings(self, guild, user):
        doc = []
        async for docu in self.sanction.find({"guild_id" : guild, "user_id": user, "event": "Strike"}):
            doc.append(docu['_id'])
        return doc or {}

    async def rm_strike_settings(self, guild, user):
        return await self.sanction.delete_many({"guild_id" : guild, "user_id": user, "event": "Strike"})
