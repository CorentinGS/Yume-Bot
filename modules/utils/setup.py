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

    async def store(self):
        set = await Settings().get_server_settings(str(self.id))

        # Settings
        set['Greet'] = self.greet
        set['bl'] = self.bl
        set['logging'] = self.logging
        set['automod'] = self.automod
        set['Display'] = self.members_count

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

        await Settings().set_server_settings(str(self.id), set)

    async def get(self):
        set = await Settings().get_server_settings(str(self.id))

        # Settings
        self.automod = set["automod"]
        self.logging = set["logging"]
        self.greet = set['Greet']
        self.members_count = set['Display']
        self.bl = set['bl']

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

        await Settings().set_server_settings(str(guild_id), set)

        return True

# TODO: Déplacer les objets ici
