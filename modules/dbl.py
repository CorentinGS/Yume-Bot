import asyncio
import json
import logging

import dbl
from discord.ext import commands

with open('./config/token.json', 'r') as cjson:
    token = json.load(cjson)


class DiscordBotsOrgAPI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.token = token['dbl']
        self.dblpy = dbl.DBLClient(self.bot, self.token)
        self.updating = self.bot.loop.create_task(self.update_stats())

        self.dblpy = dbl.DBLClient(self.bot, self.token)
        self.updating = self.bot.loop.create_task(self.update_stats())

    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count"""
        while not self.bot.is_closed():
            logger.info('Attempting to post server count')
            try:
                await self.dblpy.post_guild_count()
                logger.info('Posted server count ({})'.format(self.dblpy.guild_count()))
            except Exception as e:
                logger.exception('Failed to post server count\n{}: {}'.format(type(e).__name__, e))
            await asyncio.sleep(1800)


def setup(bot):
    global logger
    logger = logging.getLogger('bot')
    bot.add_cog(DiscordBotsOrgAPI(bot))
