import discord
from discord.ext import commands

from modules.utils.db import Settings
from modules.utils.format import Embeds

class Clan(commands.Cog):

    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config


# TODO: Clan system | Create / Edit / Add / Kick |

def setup(bot):
    bot.add_cog(Clan(bot))
