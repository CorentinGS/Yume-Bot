import discord
from discord.ext import commands
from modules.utils import checks
import json
import asyncio

with open('./config/config.json', 'r') as cjson:
    config = json.load(cjson)

OWNER = config["owner_id"]


class Report:

    conf = {}

    def __init__(self, client, config):
        self.client = client
        self.config = config

        global conf
        conf = config
        global PREFIX
        PREFIX = config["prefix"]

    @commands.command(pass_context=True)
    async def feedback(self, ctx):

        cmd = ctx.message
        await cmd.delete()
        print("FeedBack")
        auth = ctx.message.author
        guild = ctx.message.guild

        owner = await self.client.get_user_info(OWNER)

        await ctx.send("{}, Tell me your feedback".format(ctx.message.author.mention))

        print("Tell me feedback")

        def check(m):
            if m.author == ctx.message.author:
                return True
            else:
                return False

        try:
            msg = await self.client.wait_for('message', timeout=60.0, check=check)
            print('wait for')
            await owner.send("{}#{} in guild __{}__ has sent a feedback : \n **{}** \n ```{}```".format(auth.name, auth.discriminator, guild.name, msg.content, msg))
            print('sent')

        except asyncio.TimeoutError:
            await ctx.send('👎')
        else:
            await ctx.send('👍')

    @commands.command(pass_context=True)
    @checks.is_dm()
    async def debug(self, ctx,):
        channel = ctx.channel
        user = ctx.channel.recipient
        owner = await self.client.get_user_info(434421758540644382)
        await owner.send("{}#{} asked for a **debug** ! This is his informations :\n **ID** : {}".format(user.name, user.discriminator, user.id))
        return await channel.send("Can you create an issue please:\n <https://github.com/yumenetwork/Yume-Bot/issues>")


def setup(client):
    client.add_cog(Report(client, client.config))
