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
