import json

import discord
from discord.ext import commands

from modules.utils.db import Settings
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
        await ctx.message.delete()

        result = url_meteo(city)
        fetch = data_fetch(result)
        data = data_return(fetch)

        condition = f"{data['main']}, {data['description']}"

        embed = discord.Embed(
            title="Meteo",
            color=discord.Colour.dark_red()
        )
        embed.set_footer(text="Powered by https://openweathermap.org")

        embed.add_field(name='🌍 **Location**', value=f"{data['city']}, {data['country']}")
        embed.add_field(name="\N{CLOUD} **Condition**", value=condition)

        embed.add_field(name="\N{THERMOMETER} **Temperature**", value=data['temp'])
        embed.add_field(name='Temperature min', value='{}°C'.format(
            data['temp_min']))
        embed.add_field(name='Temperature max', value='{}°C'.format(
            data['temp_max']))
        embed.add_field(name='\N{FACE WITH COLD SWEAT} **Humidity**', value="{}%".format(
            data['humidity']))
        embed.add_field(name='Pressure', value="{}hPa".format(
            data['pressure']))
        embed.add_field(name='\N{SUNRISE OVER MOUNTAINS} **Sunrise (UTC)**', value=data['sunrise'])
        embed.add_field(name='\N{SUNSET OVER BUILDINGS} **Sunset (UTC)**', value=data['sunset'])
        embed.add_field(
            name='\N{DASH SYMBOL} **Wind Speed**', value="{}m/s".format(data['wind']))
        embed.add_field(name='Cloudiness', value="{}%".format(
            data['cloudiness']))

        await ctx.send(embed=embed)

    @commands.command(aliases=["mto", "weather"])
    async def meteo(self, ctx, city: str = "Paris"):
        await ctx.message.delete()

        result = url_meteo(city)
        fetch = data_fetch(result)
        data = data_return(fetch)

        condition = f"{data['main']}, {data['description']}"

        embed = discord.Embed(
            title="Meteo",
            color=discord.Colour.dark_red()
        )

        embed.set_footer(text="Powered by https://openweathermap.org")

        embed.add_field(name='🌍 **Location**', value=f"{data['city']}, {data['country']}")
        embed.add_field(name="\N{CLOUD} **Condition**", value=condition)
        embed.add_field(name='\N{FACE WITH COLD SWEAT} **Humidity**', value="{}%".format(
            data['humidity']))
        embed.add_field(name="\N{THERMOMETER} **Temperature**", value=data['temp'])
        embed.add_field(
            name='\N{DASH SYMBOL} **Wind Speed**', value="{}m/s".format(data['wind']))
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
