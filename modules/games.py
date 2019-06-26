import asyncio
<<<<<<< HEAD
=======
import random
>>>>>>> lg

import discord
from discord.ext import commands

from modules.utils.db import Settings
<<<<<<< HEAD
from modules.utils.utils import Utils, Ww, Script
=======
from modules.utils.utils import Utils


class Ww:

	@staticmethod
	async def role(liste: list):
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
>>>>>>> lg


class Games(commands.Cog):
	conf = {}
<<<<<<< HEAD

	def __init__(self, bot):
		self.bot = bot
		self.config = bot.config
=======

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

		global stolen, lover, lover_
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

		players = [1, 2, 3, 4, 5, 6, 7]
		lg = []

		for user in hub.members:
			try:
				await user.send("Welcome to the werewolf game !")
			except discord.Forbidden:
				await ctx.send("{} can't be DM, he'll not be added to the game".format(user.mention), delete_after=3)
			else:
				players.append(user.id)
				await asyncio.sleep(1)
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
				'role': config.get(user),
				'alive': True,
				'couple': False,
				'stolen': False,
				'master': False,
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

		# Start Game

		await game_chan.send("Let's start the game...")

		await game_chan.send("It's night, the whole village of {} falls asleep, "
		                     "the players close their eyes".format(ctx.guild.name))

		await game_chan.send("The thief wakes up! ")

		for user in config:
			if config.get(user) == "voleur":
				voleur = ctx.guild.get_member(int(user))
				print(voleur.name)
				if voleur is not None:
					stolen = await self.voleur_event(ctx, voleur, game)
				else:
					stolen = None

		if stolen is not None:
			player[stolen]['stolen'] = True

		await game_chan.send("The thief falls asleep")
		print("if")
		if len(players) >= 9:
			print("toto")
			for user in config:
				if config.get(user) == "cupidon":
					try:
						cupidon: discord.Member = ctx.guild.get_member(int(user))
					except TypeError:
						lover_ = None
						lover = None
					else:
						lover, lover_ = await self.cupidon_event(cupidon, game)

			if lover is not None and lover_ is not None:
				toto = str(lover.id)
				player[toto]['couple'] = True
				toto_ = str(lover.id)
				player[toto_]['couple'] = True

				await lover.send(f'Hi ! You\'re in love with {lover_.name}')
				await lover_.send(f'Hi ! You\'re in love with {lover.name}')

			await game_chan.send('The cupidon falls asleep')
		print("end")
		end: bool = False
		print("while")
		while end is False:
			await game_chan.send('The wolves wake up !')
			await lg_chan.send('You have 30s to choose someone to kill tonight !\n When your choice is done, you can '
			                   'confirm it by reacting to the next message')
			set["night"] = True
			await Settings().set_games_settings(str(ctx.message.guild.id), set)

			msg, dic = await self.lg_event(ctx, lg_chan, game)
			print(dic)
			await asyncio.sleep(30)
			prev_count: int = 0
			for reaction in msg.reactions:
				if reaction.count > prev_count:
					prev_count = reaction.count
					emote: str = reaction.emoji.name

			victim = ctx.guild.get_member(int(dic.get(emote)))
			await lg_chan.send('the victim is {}'.format(victim.name))
			set['night'] = False
			await Settings().set_games_settings(str(ctx.message.guild.id), set)

	async def lg_event(self, ctx, lg_chan: discord.TextChannel, game: discord.VoiceChannel):
		set = await Settings().get_games_settings(str(ctx.message.guild.id))
		x: int = 0
		table = {}
		reactions = []
		em = discord.Embed(timestamp=ctx.message.created_at)
		em.set_author(name='Werewolf')
		player = set["Roles"]
		for user in game.members:
			if player[str(user.id)]['role'] != "lg":
				x += 1
				emote = await self.get_emote(x)
				em.add_field(name=f"{emote}", value=f"{user.name}", inline=True)
				reactions.append(emote)
				table[emote] = user.id

		msg = await lg_chan.send(embed=em)
		for reac in reactions:
			emoji = discord.utils.get(discord.Emoji, name=reac)
			print(emoji)
			await msg.add_reaction(emoji)

		return msg, table

	@staticmethod
	async def get_emote(num: int) -> str:
		emotes = {
			1: "1️⃣",
			2: "2️⃣",
			3: "3️⃣",
			4: "4️⃣",
			5: "5️⃣",
			6: "6️⃣",
			7: "7️⃣",
			8: "8️⃣",
			9: "9️⃣",
			10: "🔟"
		}
		emote = emotes.get(num)
		return emote

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

	async def voleur_event(self, ctx, voleur: discord.Member, channel: discord.VoiceChannel):
		await voleur.send("Hi ! You can choose someone to switch roles with when he dies\n"
		                  "you can choose him by reacting to the next message")

		def check(reaction, user):
			return user == voleur and str(reaction.emoji)

		set = await Settings().get_games_settings(str(ctx.message.guild.id))
		player = set["Roles"]

		x: int = 0
		table = {}
		reactions = []
		em = discord.Embed(timestamp=ctx.message.created_at)
		print(em)
		em.set_author(name='Werewolf')
		for user in channel.members:
			if user is not voleur:
				print(user)
				x += 1
				emote = await self.get_emote(x)
				em.add_field(name=f"{emote}", value=f"{user.name}", inline=True)
				reactions.append(emote)
				table[emote] = user.id

		msg = await voleur.send(embed=em)
		print(msg)
		for reac in reactions:
			emoji = discord.utils.get(discord.Emoji, name=reac)
			await msg.add_reaction(emoji)
		try:
			r, toto = await self.bot.wait_for('reaction', check = check, timeout=15)
		except asyncio.TimeoutError:
			stolen=None
		else:
			stolen = table.get(r)

		return stolen
>>>>>>> lg



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


def setup(bot):
	bot.add_cog(Games(bot))
