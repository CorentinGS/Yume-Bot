import asyncio
import json
import random

import discord
from discord.ext import commands

from modules.utils import checks, lists
from modules.utils.db import Settings
from modules.utils.format import Embeds
from modules.utils.weather import data_fetch, data_return, url_meteo

with open('./config/config.json', 'r') as cjson:
    config = json.load(cjson)

OWNER = config["owner_id"]


class General(commands.Cog):

    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.command()
    async def ping(self, ctx):

        await ctx.send("Pong !!")

    @commands.command()
    async def pong(self, ctx):

        await ctx.send("Ping !!")



    @commands.command(aliases=['gmto', 'gweather'])
    async def gmeteo(self, ctx, city: str = "Paris"):
        tip = random.choice(lists.tip)

        await ctx.message.delete()

        result = url_meteo(city)
        fetch = data_fetch(result)
        data = data_return(fetch)

        embed = discord.Embed(
            title="Meteo",
            color=discord.Colour.dark_red()
        )
        embed.set_footer(text=f'Tip: {tip}')

        embed.add_field(name='City', value=data['city'], inline=True)
        embed.add_field(name='Country', value=data['country'], inline=True)
        embed.add_field(name='Temperature max', value="{}°C".format(
            data['temp_max']), inline=True)
        embed.add_field(name='Temperature min', value='{}°C'.format(
            data['temp_min']), inline=True)
        embed.add_field(name='Humidity', value="{}%".format(
            data['humidity']), inline=True)
        embed.add_field(name='Pressure', value="{}hPa".format(
            data['pressure']), inline=True)
        embed.add_field(name='Conditions', value=data['sky'], inline=False)
        embed.add_field(name='Sunrise', value=data['sunrise'], inline=True)
        embed.add_field(name='Sunset', value=data['sunset'], inline=True)
        embed.add_field(
            name='Wind', value="{}m/s".format(data['wind']), inline=True)
        embed.add_field(name='Cloudiness', value="{}%".format(
            data['cloudiness']), inline=True)

        await ctx.send(embed=embed)

    @commands.command(aliases=["mto", "weather"])
    async def meteo(self, ctx, city: str = "Paris"):

        tip = random.choice(lists.tip)

        await ctx.message.delete()

        result = url_meteo(city)
        fetch = data_fetch(result)
        data = data_return(fetch)

        embed = discord.Embed(
            title="Meteo",
            color=discord.Colour.dark_red()
        )
        embed.set_footer(text=f'Tip: {tip}')

        embed.add_field(name='City', value=data['city'], inline=True)
        embed.add_field(name='Country', value=data['country'], inline=True)
        embed.add_field(name='Temperature', value="{}°C".format(
            data['temp']), inline=True)
        embed.add_field(name='Conditions', value="{}".format(
            data['description']), inline=False)
        embed.add_field(
            name='Wind', value="{}m/s".format(data['wind']), inline=True)
        embed.add_field(name='Cloudiness', value="{}%".format(
            data['cloudiness']), inline=True)

        await ctx.send(embed=embed)

    @commands.command(aliases=["away", "idle"])
    async def afk(self, ctx):
        await ctx.message.delete()

        user = ctx.message.author

        setting = await Settings().get_glob_settings()
        if 'AFK' not in setting:
            setting['AFK'] = []

        setting['AFK'].append(user.id)
        await Settings().set_glob_settings(setting)
        await ctx.send(f"{user.name}, you're now AFK !", delete_after=10)

    @commands.command()
    async def jump(self, ctx, id: int, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.message.channel
        messages = await channel.history(limit=200).flatten()
        for msg in messages:
            if msg.id == id:
                await ctx.send('Url :{}'.format(msg.jump_url))


def setup(bot):
    bot.add_cog(General(bot))
