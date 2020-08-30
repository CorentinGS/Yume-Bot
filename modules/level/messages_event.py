import discord
from discord.ext import commands

from modules.sql.messages_db import MessageDB, Message
from modules.sql.rankingsdb import RankingsDB
from datetime import datetime


class Level(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config
        self._cd = commands.CooldownMapping.from_cooldown(
            1.0, 3.0, commands.BucketType.user)

    async def check(self, message: discord.Message):
        user = message.author
        if user.bot is True or message.guild is None:
            return False

        if message.guild.id not in [488765635439099914, 631811291568144384, 618414922556112916, 740622438282428416]:
            return False

        # if RankingsDB.is_ignored_chan(message.channel.id):
        #   return False

        bucket = self._cd.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            return False

        return True

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not await self.check(message):
            return

        dt = message.created_at
        time = str(dt.year) + ("0" + str(dt.month) if dt.month < 10 else str(dt.month)) + (
            "0" + str(dt.day) if dt.day < 10 else str(dt.day))
        m = Message(guild_id=message.guild.id, message_id=message.id, user_id=message.author.id,
                    channel_id=message.channel.id, time_id=int(time))

        MessageDB.insert_message(m)
        await message.channel.send("Message received")


def setup(bot):
    bot.add_cog(Level(bot))
