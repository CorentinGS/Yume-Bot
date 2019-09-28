import asyncio
import json
import logging

import dbl
from discord.ext import commands, tasks

with open('./config/token.json', 'r') as cjson:
    token = json.load(cjson)

with open('./config/config.json', 'r') as cjson:
    config = json.load(cjson)


class DiscordBotsOrgAPI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.token = token['dbl']
        self.guild = config['support']
        self.debug = config['debug']

        self.dblpy = dbl.DBLClient(self.bot, self.token)

    @tasks.loop(minutes=30.0)
    async def update_stats(self):
        logger.info('Attempting to post server count')
        try:
            await self.dblpy.post_guild_count()
            logger.info('Posted server count ({})'.format(self.dblpy.guild_count()))
        except Exception as e:
            logger.exception('Failed to post server count\n{}: {}'.format(type(e).__name__, e))
        await asyncio.sleep(1800)


    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        logger.info('Received an upvote')
        user = await self.bot.fetch_user(data["user"])
        server = self.get_guild(int(self.guild))
        for chan in server.channels:
            if chan.id == int(self.debug):
                channel = chan
        await channel.send(f"{user} has voted")

def setup(bot):
    global logger
    logger = logging.getLogger('bot')
    bot.add_cog(DiscordBotsOrgAPI(bot))
