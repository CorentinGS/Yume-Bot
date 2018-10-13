import motor.motor_asyncio


class Settings():

    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(
            'localhost', 27017)
        self.db = self.client.bot
        self.glob = self.db.glob
        self.guilds = self.db.guilds

    async def get_glob_settings(self):
        doc = await self.glob.find_one({"_id": 0})
        return doc or {}

    async def set_glob_settings(self, settings):
        return await self.glob.replace_one({"_id": 0}, settings, True)

    async def set_server_settings(self, id, settings):
        return await self.guilds.replace_one({"_id": id}, settings, True)

    async def get_server_settings(self, id):
        doc = await self.guilds.find_one({"_id": id})
        return doc or {}
