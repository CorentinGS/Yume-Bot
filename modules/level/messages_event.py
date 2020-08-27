import discord
from discord.ext import commands

from modules.level.messages_db import MessageDB, Message
from modules.sql.guilddb import GuildDB
from modules.sql.rankingsdb import RankingsDB
from modules.sql.roledb import RoleDB
from modules.sql.userdb import UserDB
from modules.utils import checks


class Level(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config
        self._cd = commands.CooldownMapping.from_cooldown(
            1.0, 3.0, commands.BucketType.user)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        user = message.author
        if user.bot is True or message.guild is None:
            return

        if message.guild.id == '264445053596991498':
            return

        if RankingsDB.is_ignored_chan(message.channel.id):
            return

        bucket = self._cd.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            return

        datetime = message.created_at
        time = str(datetime.year) + ("0" + str(datetime.month) if datetime.month < 10 else str(datetime.month)) + (
            "0" + str(datetime.day) if datetime.day < 10 else str(datetime.day))
        m = Message(guild_id=message.guild.id, message_id=message.id, user_id=message.author.id,
                    channel_id=message.channel.id, time_id=int(time))
        MessageDB.insert_message(m)


def setup(bot):
    bot.add_cog(Level(bot))
