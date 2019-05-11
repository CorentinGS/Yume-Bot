import json
import random

import aiohttp
import discord
import requests
from discord.ext import commands

from modules.utils.db import Settings
from modules.utils.format import Embeds


class Ww:

    async def role(self, liste):
        rdm = random.sample(liste, len(liste))

        Roles = {
            "vovo": rdm[0],
            "soso": rdm[1],
            "pf": rdm[2],
            "boss": rdm[3],
            "cupidon": rdm[4],
            "Lg": [],
            "Sv": []
        }
        u = len(rdm) - 1
        toto = rdm[5:u]
        t = len(toto) / 2
        g = len(toto) - 1
        lg = toto[0:int(t)]
        sv = toto[int(t):int(g)]
        Roles["Lg"].append(lg)
        Roles["Sv"].append(sv)
        return Roles


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
        game = set['game']
        try:
            chan = discord.utils.get(ctx.guild.voice_channels, id=int(game))
            await chan.delete()
        except discord.NotFound:
            pass
        except discord.Forbidden:
            return await ctx.send("I need more permissions to be able to to that")

        await Settings().set_games_settings(str(ctx.message.guild.id), set)

    @werewolf.command()
    async def start(self, ctx):

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
        if len(hub.members) < 12:
            return await ctx.send("You should be at least 12 to play !")

        # TODO: Ajouter des possibilités à moins que 15 mais virer certains roles !

        if len(hub.members) > 18:
            return await ctx.send("You can't be more than 18 !")
        '''

        cat = int(set['category'])
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(connect=False)
        }

        category = discord.utils.get(ctx.guild.categories, id=cat)

        game = await ctx.guild.create_voice_channel("Game Channel", overwrites=overwrites, user_limit=len(hub.members), category=category)

        players = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]

        for user in hub.members:
            try:
                await user.send("Welcome to the werewolf game !")
            except discord.Forbidden:
                await ctx.send("{} can't be DM, he'll not be added to the game".format(user.mention), delete_after=3)
                pass
            else:
                players.append(user.id)
                await user.move_to(game)

        set['play'] = True
        set['game'] = str(game.id)
        await Settings().set_games_settings(str(ctx.message.guild.id), set)
        await ctx.send("Game is starting")

        config = await Ww().role(players)
        await ctx.send(config)

        set["Roles"] = {
            "voyante": config.get("vovo"),
            "pf": config.get("pf"),
            "sorciere": config.get("soso"),
            "cupidon": config.get("cupidon"),
            "boss": config.get("boss"),
            "lg": config.get("Lg"),
            "sv": config.get("Sv")
        }

        await Settings().set_games_settings(str(ctx.message.guild.id), set)

        player = set["Roles"]

        voyante = self.bot.get_user(int(player["voyante"]))
        await voyante.send("You're the seer ! Every night you can see someone and discover his role... You win with the village")

        pf = self.bot.get_user(int(player["pf"]))
        await pf.send("You're the pf ! Every night you can see the werewolf chat... You win with the village")

        witch = self.bot.get_user(int(player["sorciere"]))
        await witch.send("You're the witch ! Every night you can save someone... You win with the village")

        cupidon = self.bot.get_user(int(player["cupidon"]))
        await cupidon.send("You're the cupidon ! you can setup a couple... You win with the village or the couple")

        boss = await self.bot.get_user(int(player["boss"]))
        await witch.send("You're the boss ! Your vote count as double... You win with the village")

        for user in player["lg"]:
            lg = self.bot.get_user(int(user))
            await lg.send("You're a werewolf!")

        for user in player["sv"]:
            sv = self.bot.get_user(int(user))
            await sv.send("You're a simple villager!")

        
        # TODO: Créer des salons txt pour les roles de team (lg, sv, couple !)
        # Ajuster les permissions
        # Faire le script du jeu
        # Faire les conditions de mort et de fin 
        # Définir le gagnant ^^
        lg_chan = await ctx.guild.create_text_channel("Game Channel", overwrites=lg_perm, category=category)


        while set["play"] is True:
                


def setup(bot):
    bot.add_cog(Games(bot))
