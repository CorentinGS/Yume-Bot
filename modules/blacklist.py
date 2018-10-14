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
        msg = ctx.message
        await msg.delete()

        setting = await Settings().get_glob_settings()
        if 'Blacklist' not in setting:
            setting['Blacklist'] = []

        if user.id in setting['Blacklist']:
            return await ctx.send("This user is already blacklisted")
        setting['Blacklist'].append(user.id)
        await Settings().set_glob_settings(setting)
        await ctx.send(f"{user.name}#{user.discriminator} is now blacklisted")


    @commands.command(pass_context=True)
    @checks.is_owner()
    async def blrm(self, ctx, id: int):

        banned = discord.Object(id=id)
        user = await self.bot.get_user_info(id)
        msg = ctx.message
        await msg.delete()

        setting = await Settings().get_glob_settings()
        if setting['Blacklist']:
            if user.id not in setting['Blacklist']:
                return ctx.send(f"{user.name} is not blacklisted")
            setting['Blacklist'].remove(user.id)
        await Settings().set_glob_settings(setting)
        return await ctx.send("{}#{} is now remove from blacklist".format(user.name, user.discriminator))


    async def on_member_join(self, member):
        server = member.guild
        setting = await Settings().get_glob_settings()
        if 'Blacklist' in setting:
            if member.id in setting['Blacklist']:
                await server.ban(member, reason="Blacklist")
                await member.send("you're in the blacklist ! If you think it's an error, ask here --> yumenetwork@protonmail.com")



def setup(bot):
    bot.add_cog(Blacklist(bot, bot.config))
