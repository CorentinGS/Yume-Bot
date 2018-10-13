import motor.motor_asyncio


class Settings:

    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
        self.db = client.bot

        self.users = db.users
