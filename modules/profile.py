from discord.ext import commands
import json

from modules.utils.db import Settings
from modules.utils.format import Embeds



class Profile:
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

# TODO: Ajouter l'user.id dans glob & ajouter des paramtètres en utilisant le système d'embed pour configurer le Profile !

def setup(bot):
    bot.add_cog(Profile(bot))
