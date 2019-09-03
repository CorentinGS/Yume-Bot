import discord
from discord.ext import commands


class Profile:
	def __init__(self, user: discord.User):
		# Member
		self.name = [user.name]
		self.id = user.id

		# Profile
		self.gender: str = "Unknown"


class Profiles(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


def setup(bot):
	bot.add_cog(Profiles(bot))
