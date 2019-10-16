from discord.ext import commands

class Color(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.guild_only()
    async def color(self, ctx):
        if not ctx.invoked_subcommand:
            return

def setup(bot):
    bot.add_cog(Color(bot))
