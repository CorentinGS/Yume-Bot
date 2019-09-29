import json

import dbl
import discord
import requests
from discord.ext import commands, tasks

with open('./config/token.json', 'r') as cjson:
    token = json.load(cjson)

with open('./config/config.json', 'r') as cjson:
    config = json.load(cjson)


class Dbl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.token = token['dbl']
        self.guild = config['support']
        self.debug = config['debug']

        self.dblpy = dbl.DBLClient(self.bot, self.token)

    @tasks.loop(minutes=30.0)
    async def update_stats(self):
        try:
            await self.dblpy.post_guild_count()
        except Exception as e:
            print('Failed to post server count\n{}: {}'.format(type(e).__name__, e))

    @tasks.loop(hours=12.0)
    async def dbl_vote(self):
        print('Received an upvote')
        url = f"https://discordbots.org/api/bots/{self.bot.user.id}/check"
        data = requests.get(url)

        user = await self.bot.fetch_user(data["userid"])
        server = self.bot.get_guild(int(self.guild))
        for chan in server.channels:
            if chan.id == int(self.debug):
                channel = chan
        if isinstance(user, discord.User):
            await channel.send(f"{user.name}#{user.discriminator} has voted")
        else:
            await channel.send(f"{data['user']} has voted\n `{data}`")

    @commands.command()
    async def votes(self, ctx):
        print('Up votes')
        url = f"https://discordbots.org/api/bots/{self.bot.user.id}/check"
        data = requests.get(url)
        print(data.json)

        user = await self.bot.fetch_user(data["userid"])
        server = self.bot.get_guild(int(self.guild))
        for chan in server.channels:
            if chan.id == int(self.debug):
                channel = chan
        if isinstance(user, discord.User):
            await channel.send(f"{user.name}#{user.discriminator} has voted")
        else:
            await channel.send(f"{data['user']} has voted\n `{data}`")

def setup(bot):
    bot.add_cog(Dbl(bot))
