<<<<<<< Updated upstream
=======
import asyncio
import random
from typing import List, Any, Union

import discord
>>>>>>> Stashed changes
from discord.ext import commands
import json

from modules.utils.db import Settings
<<<<<<< Updated upstream
from modules.utils.format import Embeds



class Games(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

# TODO: Ajouter des jeux automatiques !
# TODO: Trouver des partenaires de jeux
=======
from modules.utils.utils import Utils, Ww, Script


class Games(commands.Cog):
	conf = {}

	def __init__(self, bot):
		self.bot = bot
		self.config = bot.config

	@commands.group(aliases=['lg', "ww"])
	@commands.guild_only()
	@commands.has_permissions(administrator=True)
	async def werewolf(self, ctx):
		if ctx.invoked_subcommand is None:
			return

	@werewolf.command()
	async def init(self, ctx):
		set = await Settings().get_games_settings(str(ctx.message.guild.id))
		set["category"] = None
		await Settings().set_games_settings(str(ctx.message.guild.id), set)

	@werewolf.command()
	async def setup(self, ctx):
		set = await Settings().get_games_settings(str(ctx.message.guild.id))

		if not set['category'] is None:
			cat = set['category']
			try:
				chan = discord.utils.get(ctx.guild.categories, id=int(cat))
				for channel in chan.channels:
					await channel.delete()
				await chan.delete()
			except discord.Forbidden:
				return await ctx.send("I need more permissions to be able to to that")
			except discord.NotFound:
				pass

		category = await ctx.guild.create_category_channel("Werewolf")
		set['category'] = str(category.id)
		hub = await ctx.guild.create_voice_channel("Game Hub", user_limit=18, category=category)
		set['hub'] = str(hub.id)

		set['setup'] = True
		set['play'] = False
		set['night'] = False
		await Settings().set_games_settings(str(ctx.message.guild.id), set)

	@werewolf.command()
	async def stop(self, ctx):
		set = await Settings().get_games_settings(str(ctx.message.guild.id))
		set['play'] = False
		await Settings().set_games_settings(str(ctx.message.guild.id), set)
		game = set['game']
		game_ = set['Game_chan']
		game_lg = set['Lg_chan']

		await Utils().delete_voice_chan(ctx, int(game))
		await Utils().delete_text_chan(ctx, int(game_))
		await Utils().delete_text_chan(ctx, int(game_lg))

		await Settings().set_games_settings(str(ctx.message.guild.id), set)

	@werewolf.command()
	async def start(self, ctx):
		set = await Settings().get_games_settings(str(ctx.message.guild.id))

		setuped: bool = await Ww().check_setup(ctx)

		if setuped is False:
			return

		started: bool = await Ww().check_started(ctx)

		if started is True:
			return

		await ctx.send("Loading...", delete_after=5)
		await ctx.send("Remember to activate your DM or you will not be able to play", delete_after=10)

		hub: discord.VoiceChannel = discord.utils.get(ctx.guild.voice_channels, id=int(set['hub']))

		'''
		if len(hub.members) < 8 or len(hub.members) > 14:
			await ctx.send("You should be at least 8 and less than 14 to play !")
			return
		'''

		overwrites = {
			ctx.guild.default_role: discord.PermissionOverwrite(connect=False)
		}

		category: discord.CategoryChannel = discord.utils.get(ctx.guild.categories, id=int(set['category']))

		game: discord.VoiceChannel = await ctx.guild.create_voice_channel('Game Channel', overwrites=overwrites, user_limit=len(hub.members), category=category)

		players: list = await Ww().add_player(ctx, hub, game)

		set['play'] = True
		set['game'] = str(game.id)
		set['Roles'] = {}
		await Settings().set_games_settings(str(ctx.message.guild.id), set)

		await ctx.send("Game is starting")

		config = await Ww().role(players)

		# DEBUG
		await ctx.send(config)

		lg: list = await Ww().log_into_db(ctx, config)

		ow, overwrite = await Ww().setup_permissions(ctx, lg, game)

		game_chan = await ctx.guild.create_text_channel("game_channel", overwrites=overwrite, category=category)
		lg_chan = await ctx.guild.create_text_channel("lg_channel", overwrites=ow, category=category)

		set['Game_chan'] = str(game_chan.id)
		set['Lg_chan'] = str(lg_chan.id)
		await Settings().set_games_settings(str(ctx.message.guild.id), set)

		# Start Game

		await game_chan.send("Let's start the game...")

		await game_chan.send(
			f"It's night, the whole village of {ctx.guild.name} falls asleep, the players close their eyes")

		await game_chan.send("The thief wakes up! ")

		voleur = await Script(self.bot).get_voleur(ctx, config)

		if voleur is not None:
			await Script(self.bot).voleur_event(ctx, voleur, game)

		await game_chan.send("The thief falls asleep")

		cupidon = await Script(self.bot).get_cupidon(ctx, config, players)
		if cupidon is not None:
			await Script(self.bot).cupidon_event(ctx, cupidon, game, players, config)

		end: bool = False

		while end is False:
			await game_chan.send('The wolves wake up !')
			end, victim = await Script(self.bot).lg_vote(ctx, lg_chan, game, config)

	async def cupidon_event(self, cupidon: discord.Member, channel: discord.VoiceChannel):
		global m

		def msgcheck(m):
			if m.author == cupidon and m.channel == cupidon.dm_channel:
				return True
			else:
				return False

		await cupidon.send(
			'Hi, You must choose 2 people to pair up.\n Gives the place of the first lover in the voice room')

		try:
			m = await self.bot.wait_for('message', check=msgcheck, timeout=20)

		except asyncio.TimeoutError:
			await cupidon.send('👎', delete_after=3)
			lover = None
			lover_ = None
			return lover, lover_
		try:
			lover = channel.members[int(m)]
		except TypeError:
			lover = None
			lover_ = None
			return lover, lover_
		else:
			await cupidon.send('Your first lover is ' + lover.name)

		await cupidon.send('Gives the place of the first lover in the voice room')

		try:
			m = await self.bot.wait_for('message', check=msgcheck, timeout=20)

		except asyncio.TimeoutError:
			await cupidon.send('👎', delete_after=3)
			lover = None
			lover_ = None
			return lover, lover_
		try:
			lover_ = channel.members[int(m)]
		except TypeError:
			lover = None
			lover_ = None
			return lover, lover_
		else:
			await cupidon.send('Your second lover is ' + lover_.name)

			return lover, lover_

>>>>>>> Stashed changes

def setup(bot):
    bot.add_cog(Games(bot))
