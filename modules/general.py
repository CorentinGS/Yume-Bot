import discord
from discord.ext import commands
from modules.utils import checks
import json
import asyncio
import requests
from .utils.weather import url_meteo, data_fetch, data_return
from modules.utils.db import Settings

with open('./config/config.json', 'r') as cjson:
    config = json.load(cjson)

OWNER = config["owner_id"]


class General:

    conf = {}

    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

        global conf
        conf = config
        global PREFIX
        PREFIX = config["prefix"]

    @commands.command(pass_context=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ping(self, ctx):

        return await ctx.send("Pong !!")

    @commands.command(pass_context=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def pong(self, ctx):

        return await ctx.send("Ping !!")

    @commands.command(pass_context=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def feedback(self, ctx):

        cmd = ctx.message
        await cmd.delete()
        print("FeedBack")
        auth = ctx.message.author
        guild = ctx.message.guild

        owner = await self.bot.get_user_info(OWNER)

        await ctx.send("{}, Tell me your feedback".format(ctx.message.author.mention))

        print("Tell me feedback")

        def check(m):
            if m.author == ctx.message.author:
                return True
            else:
                return False

        try:
            msg = await self.bot.wait_for('message', timeout=60.0, check=check)
            print('wait for')
            await owner.send("{}#{} in guild __{}__ has sent a feedback : \n **{}** \n ```{}```".format(auth.name, auth.discriminator, guild.name, msg.content, msg))
            print('sent')

        except asyncio.TimeoutError:
            await ctx.send('👎')
        else:
            await ctx.send('👍')

    @commands.command(pass_context=True)
    @checks.is_dm()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def debug(self, ctx):
        channel = ctx.channel
        user = ctx.channel.recipient
        owner = await self.bot.get_user_info(434421758540644382)
        await owner.send("{}#{} asked for a **debug** ! This is his informations :\n **ID** : {}".format(user.name, user.discriminator, user.id))
        return await channel.send("Can you create an issue please:\n <https://github.com/yumenetwork/Yume-Bot/issues>")

    @commands.command(pass_context=True, aliases=['gmto', 'gweather'])
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def gmeteo(self, ctx, city: str = "Paris"):

        msg = ctx.message
        await msg.delete()

        result = url_meteo(city)
        fetch = data_fetch(result)
        data = data_return(fetch)

        embed = discord.Embed(
            title="Meteo",
            color=discord.Colour.dark_red()
        )

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

        return await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=["mto", "weather"])
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def meteo(self, ctx, city: str = "Paris"):

        msg = ctx.message
        await msg.delete()

        result = url_meteo(city)
        fetch = data_fetch(result)
        data = data_return(fetch)

        embed = discord.Embed(
            title="Meteo",
            color=discord.Colour.dark_red()
        )

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

        return await ctx.send(embed=embed)

    @commands.command(pass_context = True, aliases=["away", "idle"])
    async def afk(self, ctx, *, content: str = None):

        msg = ctx.message
        await msg.delete()

        user = ctx.message.author

        setting = await Settings().get_users_settings(user.id)
        setting['afk'] = True
        setting['afk_reason'] = content
        await Settings().set_users_settings(user.id, setting)
        await ctx.send('{} is now afk with the reason {}'.format(user.name, content))

    async def on_typing(self, channel, user, when):
        setting = await Settings().get_users_settings(user.id)
        if setting.get['afk', True] :
            setting['afk'] = False
            setting['afk_reason'] = None
            await Settings().set_users_settings(user_id, setting)
            await ctx.send(f"{user.mention}, welcome back !")

    async def on_message(self, message):


def setup(bot):
    bot.add_cog(General(bot, bot.config))
