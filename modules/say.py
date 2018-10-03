import discord
from discord.ext import commands
from modules.utils import checks
import json


class Say:

    conf = {}

    def __init__(self, client, config):
        self.client = client
        self.config = config

        global conf
        conf = config

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def echo(self, ctx, *, content):

        msg = ctx.message

        try:
            await msg.delete()
            return await ctx.send(content)

        except:
            pass

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def dm(self, ctx, user: discord.Member, *, content):

        msg = ctx.message

        try:
            await msg.delete()
            await ctx.send("{} has been dm".format(user.display_name))
            return await user.send(content)

        except:
            pass

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def send(self, ctx, channel: discord.TextChannel, *, content):

        msg = ctx.message

        try:
            await msg.delete()
            return await channel.send(content)

        except:
            pass


def setup(client):
    client.add_cog(Say(client, client.config))
