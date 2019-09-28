from discord.ext import commands

from modules.utils import checks


class Security(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.group()
    @checks.is_admin()
    async def gateway(self, ctx):
        return


# TODO: Faire les commandes de sécurité...

    @commands.command()
    @checks.is_admin()
    async def lock(self, ctx):
        return

def setup(bot):
    bot.add_cog(Security(bot))
