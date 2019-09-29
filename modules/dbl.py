import json

import dbl
import discord
from discord.ext import commands, tasks

with open('./config/token.json', 'r') as cjson:
    token = json.load(cjson)

with open('./config/config.json', 'r') as cjson:
    config = json.load(cjson)


class DiscordBotsOrgAPI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.token = token['dbl']
        self.web = token['webhook_dbl']
        self.guild = config['support']
        self.debug = config['debug']

        self.dblpy = dbl.DBLClient(self.bot, self.token, webhook_path='/webhook', webhook_auth=self.web,
                                   webhook_port=27018)

    @tasks.loop(minutes=30.0)
    async def update_stats(self):
        try:
            await self.dblpy.post_guild_count()
        except Exception as e:
            print('Failed to post server count\n{}: {}'.format(type(e).__name__, e))

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        print('Received an upvote')
        user = await self.bot.fetch_user(data["user"])
        server = self.bot.get_guild(int(self.guild))
        for chan in server.channels:
            if chan.id == int(self.debug):
                channel = chan
        if isinstance(user, discord.User):
            await channel.send(f"{user.name}#{user.discriminator} has voted")
        else:
            await channel.send(f"{data['user']} has voted\n `{data}`")

    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        print('Received a test upvote')


def setup(bot):
    bot.add_cog(DiscordBotsOrgAPI(bot))
