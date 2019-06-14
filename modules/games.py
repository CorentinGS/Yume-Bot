import asyncio
import random

import discord
from discord.ext import commands

from modules.utils.db import Settings
from modules.utils.utils import Utils


class Ww:

	@staticmethod
	async def role(liste):
		rdm = random.sample(liste, len(liste))
		lg = []
		sv = []

		roles = {
			str(rdm[0]): "voleur",
			str(rdm[1]): "soso",
			str(rdm[2]): "vovo",
			str(rdm[3]): "boss"
		}

		if len(rdm) == 8:
			lg = rdm[3:5]
			sv = rdm[5:7]

		elif len(rdm) == 9:

			roles[str(rdm[4])]: "cupidon"
			lg = rdm[4:6]
			sv = rdm[6:8]

		elif len(rdm) == 10:
			roles[str(rdm[4])]: "cupidon"
			sv = rdm[4:6]
			lg = rdm[6:9]

		elif len(rdm) == 11:
			roles[str(rdm[4])]: "chasseur"
			roles[str(rdm[5])]: "cupidon"
			sv = rdm[5:7]
			lg = rdm[7:10]

		elif len(rdm) == 12:
			roles[str(rdm[4])]: "chasseur"
			roles[str(rdm[5])]: "cupidon"
			sv = rdm[5:8]
			lg = rdm[8:11]

		elif len(rdm) == 13:
			roles[str(rdm[4])]: "chasseur"
			roles[str(rdm[5])]: "cupidon"
			sv = rdm[5:8]
			lg = rdm[8:11]
			roles[str(rdm[12])]: "enfant_sauvage"

		elif len(rdm) == 14:
			roles[str(rdm[4])]: "chasseur"
			roles[str(rdm[5])]: "cupidon"
			sv = rdm[5:8]
			lg = rdm[8:11]
			roles[str(rdm[12])]: "enfant_sauvage"
			roles[str(rdm[13])]: "pf"

		for gl in lg:
			roles[str(gl)] = "lg"
		for vs in sv:
			roles[str(vs)] = "sv"

		return roles


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

		'''
        try:
            chan = discord.utils.get(ctx.guild.voice_channels, id=int(game))
            await chan.delete()
        except discord.NotFound:
            pass
        except discord.Forbidden:
            return await ctx.send("I need more permissions to be able to to that")

        try:
            chan_ = discord.utils.get(ctx.guild.text_channels, id=int(game_))
            await chan_.delete()
        except discord.NotFound:
            pass
        except discord.Forbidden:
            return await ctx.send("I need more permissions to be able to to that")
        '''

		await Settings().set_games_settings(str(ctx.message.guild.id), set)

	@werewolf.command()
	async def start(self, ctx):

		global voleur
		set = await Settings().get_games_settings(str(ctx.message.guild.id))

		if not 'setup' in set:
			set['setup'] = False
			await Settings().set_games_settings(str(ctx.message.guild.id), set)
			return await ctx.send("You must setup your guild before starting the game !\nUse **--werewolf setup**")

		if set['setup'] is False:
			return await ctx.send("You must setup your guild before starting the game !\nUse **--werewolf setup**")

		_hub = int(set["hub"])

		hub = discord.utils.get(ctx.guild.voice_channels, id=_hub)

		if hub is None:
			return await ctx.send("You must setup your guild before starting the game !\nUse **--werewolf setup**")

		if not 'play' in set:
			set['play'] = False

		if set['play'] is True:
			return await ctx.send("A game is already started")

		await ctx.send("Loading...", delete_after=5)
		await ctx.send("Remember to activate your DM or you will not be able to play", delete_after=10)

		'''
        if len(hub.members) < 8:
            return await ctx.send("You should be at least 8 to play !")

        # TODO: Ajouter des possibilités à moins que 15 mais virer certains roles !

        if len(hub.members) > 14:
            return await ctx.send("You can't be more than 14 !")
        '''

		cat = int(set['category'])
		overwrites = {
			ctx.guild.default_role: discord.PermissionOverwrite(connect=False)
		}

		category = discord.utils.get(ctx.guild.categories, id=cat)

		game = await ctx.guild.create_voice_channel("Game Channel", overwrites=overwrites, user_limit=len(hub.members),
		                                            category=category)

		players = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 10]
		lg = []

		for user in hub.members:
			try:
				await user.send("Welcome to the werewolf game !")
			except discord.Forbidden:
				await ctx.send("{} can't be DM, he'll not be added to the game".format(user.mention), delete_after=3)
			else:
				players.append(user.id)
				await user.move_to(game)

		set['play'] = True
		set['game'] = str(game.id)
		set['Roles'] = {}
		await Settings().set_games_settings(str(ctx.message.guild.id), set)
		await ctx.send("Game is starting")

		config = await Ww().role(players)

		# DEBUG
		await ctx.send(config)

		player = set["Roles"]
		category = discord.utils.get(ctx.guild.categories, id=cat)

		overwrite = {
			ctx.guild.default_role: discord.PermissionOverwrite(
				read_messages=False)
		}

		ow = {
			ctx.guild.default_role: discord.PermissionOverwrite(
				read_messages=False)
		}

		for user in config:
			player[user] = {
				"role": config.get(user),
				"alive": True,
				"couple": False
			}

			if config.get(user) == "lg":
				lg.append(user)

			'''
            try:
                u = ctx.guild.get_member(int(user))
            except discord.NotFound:
                pass
            else:
                await u.send("You're the {}".format(config.get(user)))
            '''

		category = discord.utils.get(ctx.guild.categories, id=cat)

		for u in game.members:
			overwrite[u] = discord.PermissionOverwrite(read_messages=True)

			if str(u.id) in lg:
				ow[u] = discord.PermissionOverwrite(read_messages=True)

		game_chan = await ctx.guild.create_text_channel("game_channel", overwrites=overwrite, category=category)

		set['Game_chan'] = str(game_chan.id)

		lg_chan = await ctx.guild.create_text_channel("lg_channel", overwrites=ow, category=category)

		set['Lg_chan'] = str(lg_chan.id)

		await Settings().set_games_settings(str(ctx.message.guild.id), set)

		# end = False

		# Start Game

		await game_chan.send("Let's start the game...")

		await game_chan.send("It's night, the whole village of {} falls asleep, "
		                     "the players close their eyes".format(ctx.guild.name))

		await game_chan.send("the thief wakes up! ")

		for user in config:
			if user == "voleur":
				voleur = await ctx.get_member(int(user))

		stolen = await self.voleur_event(self, voleur, game)

		if stolen is not None:
			toto = config.get(stolen.id)
			player[toto]['stolen'] = True

		await game_chan.send("The thief fall asleep")

	async def voleur_event(self, ctx, voleur: discord.Member, channel: discord.VoiceChannel):

		global m
		await voleur.send("Hi ! You can choose someone to switch roles with when he dies\n"
		                  "Gives his place in the voice room")

		def msgcheck(m):
			if m.author == voleur:
				return True
			else:
				return False

		try:
			m = await self.bot.wait_for('message', check=msgcheck, timeout=60)

		except asyncio.TimeoutError:
			await voleur.send('👎', delete_after=3)

		try:
			stolen = channel.members[int(m)]
		except TypeError:
			stolen = None
		else:
			await voleur.send("Your victim is " + stolen.name)

		return stolen


def setup(bot):
	bot.add_cog(Games(bot))
