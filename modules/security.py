from discord.ext import commands

from modules.utils import checks


class Security(commands.Cog):
	conf = {}

	def __init__(self, bot):
		self.bot = bot
		self.config = bot.config

	@commands.group()
	@checks.is_admin()
	async def security(self, ctx):
		return


# TODO: Faire les commandes de sécurité...


def setup(bot):
	bot.add_cog(Security(bot))
