import asyncio
import random
from typing import List, Optional, Any, Dict

import discord

from modules.utils.db import Settings


class Utils:

	@staticmethod
	async def delete_voice_chan(ctx, id: int):
		try:
			chan = discord.utils.get(ctx.guild.voice_channels, id=id)
			await chan.delete()
		except discord.NotFound:
			return
		except discord.Forbidden:
			return await ctx.send("I need more permissions to be able to to that", delete_after=5)

	@staticmethod
	async def delete_text_chan(ctx, id: int):
		try:
			chan = discord.utils.get(ctx.guild.text_channels, id=id)
			await chan.delete()
		except discord.NotFound:
			return
		except discord.Forbidden:
			return await ctx.send("I need more permissions to be able to to that", delete_after=5)

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

	@staticmethod
	async def check_setup(ctx) -> bool:
		set = await Settings().get_games_settings(str(ctx.message.guild.id))

		if not 'setup' in set:
			set['setup'] = False
			await Settings().set_games_settings(str(ctx.message.guild.id), set)
			await ctx.send("You must setup your guild before starting the game !\nUse **--werewolf setup**")
			setup = False

		elif set['setup'] is False:
			await ctx.send("You must setup your guild before starting the game !\nUse **--werewolf setup**")
			setup = False

		else:
			_hub = int(set["hub"])

			hub: discord.VoiceChannel = discord.utils.get(ctx.guild.voice_channels, id=_hub)

			if hub is None:
				await ctx.send("You must setup your guild before starting the game !\nUse **--werewolf setup**")
				setup = False

			else:
				setup = True
		return setup

	@staticmethod
	async def check_started(ctx) -> bool:
		set = await Settings().get_games_settings(str(ctx.message.guild.id))

		if not 'play' in set:
			set['play'] = False
			started = False

		elif set['play'] is True:
			await ctx.send("A game is already started")
			started = True

		else:
			started = False

		return started

	@staticmethod
	async def add_player(ctx, channel: discord.VoiceChannel, game: discord.VoiceChannel):
		players: List[int] = [1, 2, 3, 4, 5, 6]

		for user in channel.members:
			try:
				await user.send("Welcome to the werewolf game !")
			except discord.Forbidden:
				await ctx.send("{} can't be DM, he'll not be added to the game".format(user.mention), delete_after=3)
			else:
				players.append(user.id)
				await asyncio.sleep(1)
				await user.move_to(game)

		return players

	@staticmethod
	async def log_into_db(ctx, config: dict):
		set = await Settings().get_games_settings(str(ctx.message.guild.id))
		lg: List[str] = []

		player = set["Roles"]

		for user in config:
			player[str(user)] = {
				'role': config.get(user),
				'alive': True,
				'couple': False,
				'stolen': False,
				'master': False,
			}

			print(config)
			print(player[str(user)])

			if config.get(user) == "lg":
				lg.append(str(user))

			'''
			patate = ctx.guild.get_member(int(user))
			await patate.send("You're the {}".format(config.get(user)))
			'''

		return lg

	@staticmethod
	async def setup_permissions(ctx, lg: list, game: discord.VoiceChannel):
		overwrite = {
			ctx.guild.default_role: discord.PermissionOverwrite(
				read_messages=False)
		}

		ow = {
			ctx.guild.default_role: discord.PermissionOverwrite(
				read_messages=False)
		}

		for u in game.members:
			overwrite[u] = discord.PermissionOverwrite(read_messages=True)

			if str(u.id) in lg:
				ow[u] = discord.PermissionOverwrite(read_messages=True)

		return ow, overwrite


class Script:

	def __init__(self, bot):
		self.bot = bot
		self.config = bot.config

	@staticmethod
	async def get_voleur(ctx, config: dict):
		global voleur
		for user in config:
			if config.get(user) == "voleur":
				voleur = discord.utils.get(ctx.guild.members, id=int(user))

		return voleur

	@staticmethod
	async def get_cupidon(ctx, config: dict, players: list):
		global cupidon
		if len(players) >= 9:
			for user in config:
				if config.get(user) == "cupidon":
					cupidon = discord.utils.get(ctx.guild.members, id=int(user))
		else:
			cupidon = None

		return cupidon

	async def voleur_event(self, ctx, voleur: discord.Member, channel: discord.VoiceChannel):
		set = await Settings().get_games_settings(str(ctx.message.guild.id))

		def check(reaction, user):
			return user == voleur

		await voleur.send(
			'Hi ! You can choose someone to switch roles with when he dies\n you can choose him by reacting to the next message')

		x: int = 0
		table = {}
		reactions = []

		em = discord.Embed(timestamp=ctx.message.created_at)
		em.set_author(name='Werewolf')

		for user in channel.members:
			if user.id != voleur.id:
				x += 1
				emote = f"{x}\N{COMBINING ENCLOSING KEYCAP}"
				table[emote] = user.id
				reactions.append(emote)
				em.add_field(name=f"{emote}", value=f"{user.name}", inline=True)

		msg = await voleur.send(embed=em)

		for reac in reactions:
			await msg.add_reaction(reac)

		try:
			reaction, user = await self.bot.wait_for('reaction', check=check, timeout=15)
		except asyncio.TimeoutError:
			stolen = None
		else:
			print(reaction.emoji)
			stolen = table.get(reaction.emoji)
		set['Roles'][stolen]['stolen'] = True
		await Settings().set_games_settings(str(ctx.message.guild.id), set)

	async def cupidon_event(self, ctx, cupidon: discord.Member, channel: discord.VoiceChannel, players: list, config: dict):
		print('toto')

	async def lg_vote(self, ctx, lg_chan: discord.TextChannel, game: discord.VoiceChannel, config: dict):
		end = False
		set = await Settings().get_games_settings(str(ctx.message.guild.id))
		await lg_chan.send('You have 30s to choose someone to kill tonight !\n When your choice is done, you can '
							   'confirm it by reacting to the next message')
		set["night"] = True
		await Settings().set_games_settings(str(ctx.message.guild.id), set)
		print('set')
		msg, dic = await self.lg_event(ctx, lg_chan, game)
		print("lg_event")
		await asyncio.sleep(30)

		prev_count: int = 0
		for reaction in msg.reactions:
			if reaction.count > prev_count:
				prev_count = reaction.count
				emote: str = reaction.emoji

		victim = ctx.guild.get_member(int(dic.get(emote)))
		await lg_chan.send('the victim is {}'.format(victim.name))
		set['night'] = False
		await Settings().set_games_settings(str(ctx.message.guild.id), set)

		return end, victim

	@staticmethod
	async def lg_event(ctx, lg_chan: discord.TextChannel, game: discord.VoiceChannel):
		set = await Settings().get_games_settings(str(ctx.message.guild.id))
		x: int = 0
		table = {}
		reactions = []

		em = discord.Embed(timestamp=ctx.message.created_at)
		em.set_author(name='Werewolf')
		print("embed")
		players = set['Roles']

		for user in game.members:
			print(user.name)
			toto = players[str(user.id)]
			if toto['role'] != "lg":
				x += 1
				print(x)
				emote = f"{x}\N{COMBINING ENCLOSING KEYCAP}"
				reactions.append(emote)
				table[emote] = user.id
				em.add_field(name=f"{emote}", value=f"{user.name}", inline=True)
		print(reactions)
		msg = await lg_chan.send(embed=em)
		for reac in reactions:
			print(reac)
			await msg.add_reaction(reac)

		return msg, table


