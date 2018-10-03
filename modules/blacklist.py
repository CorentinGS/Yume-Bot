import discord
from discord.ext import commands
from modules.utils import checks
import json
import pymongo
from pymongo import MongoClient


class Blacklist:

    conf = {}

    def __init__(self, client, config):
        self.client = client
        self.config = config

        global conf
        conf = config

    global db
    global mongo
    global users
    mongo = MongoClient('mongo', 27017)
    db = mongo.bot
    users = db.users

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def bladd(self, ctx, id: int, *, reason: str = None):

        banned = discord.Object(id=id)
        member = await self.client.get_user_info(id)
        message = ctx.message
        message.delete()

        users.update_one(
            {
                'User_id': id
            },
            {
                '$set': {
                    'User': '{}#{}'.format(member.name, member.discriminator),
                    'User_id': member.id,

                    'Blacklist': True,
                    'Reason': reason
                }
            },
            True
        )

        return await ctx.send("{}#{} is now in the blacklist".format(member.name, member.discriminator))

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def blrm(self, ctx, id: int):

        banned = discord.Object(id=id)
        member = await self.client.get_user_info(id)
        message = ctx.message
        message.delete()

        users.update(
            {'User_id': id},
            {'$set': {"Blacklist": False, 'User': '{}#{}'.format(
                member.name, member.discriminator), "Reason": 'None'}}
        )
        return await ctx.send("{}#{} is now remove from blacklist".format(member.name, member.discriminator))

    @commands.command(pass_context=True)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def blacklist(self, ctx):

        blacklisted = users.find({'Blacklist': True})

        for bl in blacklisted:
            await ctx.guild.ban(discord.Object(id=bl["User_id"]))
            # await ctx.send('{} has been banned'.format(bl['User']))

        return

    @commands.command(pass_context=True)
    @commands.guild_only()
    @checks.is_owner()
    async def bllist(self, ctx):
        message = ctx.message
        message.delete()

        blacklisted = users.find({'Blacklist': True})
        for bl in blacklisted:
            await ctx.send('{} is blacklisted'.format(bl['User']))

        return

    @commands.command(pass_context=True)
    @commands.guild_only()
    @checks.is_owner()
    async def getban(self, ctx):

        message = ctx.message
        message.delete()
        banned = await ctx.guild.bans()
        for bl in banned:
            users.update_one(
                {
                    'User_id': bl.user.id
                },
                {
                    '$set': {
                        'User': '{}#{}'.format(bl.user.name, bl.user.discriminator),
                        'User_id': bl.user.id,

                        'Blacklist': True,
                        'Reason': "getban"
                    }
                },
                True
            )

        await ctx.send("Users is now in the blacklist ! ")

        return


def setup(client):
    client.add_cog(Blacklist(client, client.config))
