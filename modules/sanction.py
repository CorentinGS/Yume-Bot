import json
import os
import random

import discord
from discord.ext import commands

from modules.utils import checks, lists


class Sanction:

    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

# TODO: Ajouter les "event" dans la base

def setup(bot):
    bot.add_cog(Sanction(bot))