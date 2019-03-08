from discord.ext import commands
import json

from modules.utils.db import Settings
from modules.utils.format import Embeds



class Games(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

# TODO: Ajouter des jeux automatiques !
# TODO: Trouver des partenaires de jeux

def setup(bot):
    bot.add_cog(Games(bot))
