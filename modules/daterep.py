import discord
from discord.ext import commands
import json
import datetime
from romme import RepublicanDate


class Date:

    conf = {}

    def __init__(self, client, config):
        self.client = client
        self.config = config

        global conf
        conf = config

    @commands.command(pass_context=True)
    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def rd(self, ctx):

        msg = ctx.message
        today = datetime.date.today()
        print(today.year)
        rd = RepublicanDate.from_gregorian(today.year, today.month, today.day)

        print(rd)

        try:
            await ctx.send(rd)
            await msg.delete()
            return

        except:
            pass


def setup(client):
    client.add_cog(Date(client, client.config))
