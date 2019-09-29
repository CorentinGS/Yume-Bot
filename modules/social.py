from discord.ext import commands


class Social(commands.Cog):

    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config



def setup(bot):
    bot.add_cog(Social(bot))