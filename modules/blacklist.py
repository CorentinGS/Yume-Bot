from discord.ext import commands
from modules.utils import checks

from modules.utils.db import Settings


class Blacklist:

    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.group(aliases=['bl'])
    @checks.is_owner()
    async def blacklist(self, ctx):
        if ctx.invoked_subcommand is None:
            return

    @blacklist.command()
    @checks.is_owner()
    async def add(self, ctx, id: int):

        user = await self.bot.get_user_info(id)
        await ctx.message.delete()

        setting = await Settings().get_glob_settings()
        if 'Blacklist' not in setting:
            setting['Blacklist'] = []

        if user.id in setting['Blacklist']:
            return await ctx.send("This user is already blacklisted")
        setting['Blacklist'].append(user.id)
        await Settings().set_glob_settings(setting)
        await ctx.send(f"{user.name}#{user.discriminator} is now blacklisted")

    @blacklist.command(aliases=['remove'])
    @checks.is_owner()
    async def rm(self, ctx, id: int):

        user = await self.bot.get_user_info(id)
        await ctx.message.delete()

        setting = await Settings().get_glob_settings()
        if setting['Blacklist']:
            if user.id not in setting['Blacklist']:
                return ctx.send(f"{user.name} is not blacklisted")
            setting['Blacklist'].remove(user.id)
        await Settings().set_glob_settings(setting)
        await ctx.send("{}#{} is now remove from blacklist".format(user.name, user.discriminator))


def setup(bot):
    bot.add_cog(Blacklist(bot))
