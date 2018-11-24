import discord
from discord.ext import commands

import json
import asyncio
import random

from .utils.weather import url_meteo, data_fetch, data_return

from modules.utils.db import Settings
from modules.utils.format import Embeds
from modules.utils import checks, lists



with open('./config/config.json', 'r') as cjson:
    config = json.load(cjson)

OWNER = config["owner_id"]
tip = random.choice(lists.tip)


class General:

    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config


    @commands.command()
    #  @commands.cooldown(1, 10, commands.BucketType.user)
    async def ping(self, ctx):

        await ctx.send("Pong !!")

    @commands.command()
    #  @commands.cooldown(1, 10, commands.BucketType.user)
    async def pong(self, ctx):

        await ctx.send("Ping !!")

    @commands.command()
    #  @commands.cooldown(1, 30, commands.BucketType.user)
    async def feedback(self, ctx):

        await ctx.message.delete()

        auth = ctx.message.author
        guild = ctx.message.guild

        owner = await self.bot.get_user_info(OWNER)

        await ctx.send("{}, Tell me your feedback".format(ctx.message.author.mention), delete_after=70)

        def check(m):
            if m.author == ctx.message.author:
                return True
            else:
                return False

        try:
            msg = await self.bot.wait_for('message', timeout=60.0, check=check)

        except asyncio.TimeoutError:
            await ctx.send('👎')
            success = False
            return

        else:
            success = True
            await ctx.send('👍')


        msg.delete()
        em = await Embeds().format_feedback_embed(ctx, auth, guild, success, msg)
        await owner.send(embed=em)

    @commands.command(aliases=['gmto', 'gweather'])
    #  @commands.cooldown(1, 20, commands.BucketType.user)
    async def gmeteo(self, ctx, city: str = "Paris"):

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
    #  @commands.cooldown(1, 20, commands.BucketType.user)
    async def meteo(self, ctx, city: str = "Paris"):

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
        messages = await channel.history(limit = 200).flatten()
        for msg in messages:
            if msg.id == id:
                await ctx.send('Url :{}'.format(msg.jump_url))


def setup(bot):
    bot.add_cog(General(bot))
