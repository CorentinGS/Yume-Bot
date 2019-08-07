from discord.ext import commands

from modules.utils import checks
from modules.utils.db import Settings


class Custom(commands.Cog):

	conf = {}

	def __init__(self, bot):
		self.bot = bot
		self.config = bot.config

	@commands.command()
	@checks.is_vip()
	async def game_viewer(self, ctx):
		toto = await ctx.send(f"{ctx.author.mention} has created a game viewer ! "
		                      f"If you want to join the queue you just need to react to the message")
		await toto.add_reaction("✅")

		set = await Settings().get_custom_settings(str(ctx.guild.id))
		set["message_id"] = toto.id
		set["game_viewer"] = True
		set["viewers"] = {}
		await Settings().set_custom_settings(str(ctx.guild.id), set)

	@commands.Cog.listener()
	async def on_reaction_add(self, reaction, user):

		set = await Settings().get_custom_settings(str(reaction.message.guild.id))
		if 'game_viewer' not in set:
			return
		if not set["game_viewer"] is True or not reaction.message.id == set["message_id"]:
			return

		viewers = set["viewers"]
		x = len(viewers)
		viewers[str(x)] = user.id

		await Settings().set_custom_settings(str(reaction.message.guild.id), set)

	@commands.command()
	@checks.is_vip()
	async def get_viewer(self, ctx, number: int = 4):
		players = []
		set = await Settings().get_custom_settings(str(ctx.guild.id))
		if not set["game_viewer"] is True:
			return await ctx.send("You must start a game viewer !")
		viewers = set["viewers"]
		for viewer in viewers.values():
			member = await self.bot.fetch_user(int(viewer))
			players.append(f"{member.mention}")

		await ctx.send(players[0:number])


def setup(bot):
	bot.add_cog(Custom(bot))