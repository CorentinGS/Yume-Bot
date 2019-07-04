import asyncio

import discord
from discord.ext import commands

from modules.sanction import Sanction
from modules.utils import checks
from modules.utils.db import Settings
from modules.utils.format import Embeds


class Reactions(commands.Cog):
	conf = {}

	def __init__(self, bot):
		self.bot = bot
		self.config = bot.config

	@commands.command()
	@commands.guild_only()
	@checks.is_admin()
	async def arr(self, ctx, message_id: int, role: discord.Role, emoji: str):
		# get emoji
		set = await Settings().get_reaction_settings(str(ctx.guild.id))
		await ctx.send(f"{emoji}, {role}")
		set[str(message_id)] = {
			"emoji": emoji.id,
			"role": role.id
		}

		await Settings().set_reaction_settings(str(ctx.guild.id), set)


def setup(bot):
	bot.add_cog(Reactions(bot))
