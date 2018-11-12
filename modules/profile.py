from discord.ext import commands
import json

from modules.utils.db import Settings
from modules.utils.format import Embeds



class Profile:
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.group()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def profile(self, ctx):
        if ctx.invoked_subcommand is None:
            return

    @profile.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def gender(self, ctx, arg: str = None):
        user = str(ctx.message.author.id)
        set = await Settings().get_user_settings(user)

        if arg.lower().startswith('male'):
            set['gender'] = "male"
        elif arg.lower().startswith('female'):
            set['gender'] = "female"
        elif arg.lower().startswith('trans'):
            set['gender'] = "transgender"
        elif arg.lower().startswith('cat'):
            set['gender'] = "cat"
        else:
            return await ctx.send(f'{arg} is not a valid argument !')

        await Settings().set_user_settings(user, set)





# TODO: Ajouter l'user.id dans glob & ajouter des paramtètres en utilisant le système d'embed pour configurer le Profile !

def setup(bot):
    bot.add_cog(Profile(bot))
