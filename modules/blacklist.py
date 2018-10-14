import discord
from discord.ext import commands
from modules.utils import checks
import json

from modules.utils.db import Settings


class Blacklist:

    conf = {}

    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

        global conf
        conf = config

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def bladd(self, ctx, id: int):

        banned = discord.Object(id=id)
        user = await self.bot.get_user_info(id)
        message = ctx.message
        await message.delete()

        setting = await Settings().get_glob_settings()
        if 'Blacklist' not in setting:
            setting['Blacklist'] = []

        if user.id in setting['Blacklist']:
            return await ctx.send("This user is already blacklisted")
        setting['Blacklist'].append(user.id)
        await Settings().set_glob_settings(setting)
        return await ctx.send(f"{user.name}#{user.discriminator} is now blacklisted")


    @commands.command(pass_context=True)
    @checks.is_owner()
    async def blrm(self, ctx, id: int):

        banned = discord.Object(id=id)
        user = await self.bot.get_user_info(id)
        message = ctx.message
        message.delete()

        setting = await Settings().get_glob_settings()
        if setting['Blacklist']:
            if user.id not in setting['Blacklist']:
                return ctx.send(f"{user.name} is not blacklisted")
            setting['Blacklist'].remove(user.id)
        await Settings().set_glob_settings(setting)
        return await ctx.send("{}#{} is now remove from blacklist".format(user.name, user.discriminator))


def setup(bot):
    bot.add_cog(Blacklist(bot, bot.config))
