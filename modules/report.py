import discord
from discord.ext import commands
from modules.utils import checks
import json
import asyncio


class Report:

    conf = {}

    def __init__(self, client, config):
        self.client = client
        self.config = config

        global conf
        conf = config
        global PREFIX
        PREFIX = config["prefix"]



    @commands.command(pass_context = True)
    async def feedback(self, ctx):

        msg = ctx.message
        await msg.delete()
        user = ctx.message.author


        try :
            await ctx.send("{}, look at your DM".format(user.mention))
            return await user.send('Hey ! You asked me for a bug report ! Please type the command **{}debug** and follow the instructions...'.format(PREFIX))

        except discord.Forbidden:
            return await ctx.send('I cannot DM you ! Please switch your DM permissions to **ALLOWED** !')


    @commands.command(pass_context = True)
    @checks.is_dm()
    async def debug(self, ctx,):
        channel = ctx.channel
        user = ctx.channel.recipient
        owner = await self.client.get_user_info(434421758540644382)
        await owner.send(
        "{}#{} asked for a **debug** ! This is his informations :\n **ID** : {}".format(user.name, user.discriminator, user.id))
        return await channel.send("Can you fill the feedback please:\n <https://anon.to/0fyO7H>")



def setup(client):
    client.add_cog(Report(client, client.config))
