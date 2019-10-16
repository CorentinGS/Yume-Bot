import discord
from discord.ext import commands


class Profile:
    def __init__(self, user: discord.User):
        # Member
        self.name = [user.name]
        self.id = user.id

        # Profile
        self.gender: str = "Unknown"
        self.age: int = 0
        self.desc: str = 'None'

        # Reputation
        self.rep: int = 0

        # Settings
        self.vip: bool = False

        # Marriage
        self.married: bool = False
        self.lover: int = 0



class Profiles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.group()
    @commands.guild_only()
    async def marriage(self, ctx):
        if ctx.invoked_subcommand is None:
            return

    @marriage.command()
    @commands.guild_only()
    async def ask(self, ctx):
        return

def setup(bot):
    bot.add_cog(Profiles(bot))
