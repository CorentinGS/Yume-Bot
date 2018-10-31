import discord
from discord.ext import commands
from modules.utils import checks
import json
import asyncio
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

    @commands.command()
    #  @commands.cooldown(1, 10, commands.BucketType.user)
    async def ping(self, ctx):

        return await ctx.send("Pong !!")

    @commands.command()
    #  @commands.cooldown(1, 10, commands.BucketType.user)
    async def pong(self, ctx):

        return await ctx.send("Ping !!")

    @commands.command()
    #  @commands.cooldown(1, 30, commands.BucketType.user)
    async def feedback(self, ctx):

        cmd = ctx.message
        await cmd.delete()
        print("FeedBack")
        auth = ctx.message.author
        guild = ctx.message.guild

        owner = await self.bot.get_user_info(OWNER)

        await ctx.send("{}, Tell me your feedback".format(ctx.message.author.mention), delete_after=70)

        print("Tell me feedback")

        def check(m):
            if m.author == ctx.message.author:
                return True
            else:
                return False

        try:
            msg = await self.bot.wait_for('message', timeout=60.0, check=check)
            await owner.send("{}#{} in guild __{}__ has sent a feedback : \n **{}** \n ```{}```".format(auth.name, auth.discriminator, guild.name, msg.content, msg))

        except asyncio.TimeoutError:
            await ctx.send('👎')
        else:
            await ctx.send('👍')

    @commands.command()
    @checks.is_dm()
    #  @commands.cooldown(1, 60, commands.BucketType.user)
    async def debug(self, ctx):
        channel = ctx.channel
        user = ctx.channel.recipient
        owner = await self.bot.get_user_info(434421758540644382)
        await owner.send("{}#{} asked for a **debug** ! This is his informations :\n **ID** : {}".format(user.name, user.discriminator, user.id))
        return await channel.send("Can you create an issue please:\n <https://github.com/yumenetwork/Yume-Bot/issues>")

    @commands.command(aliases=['gmto', 'gweather'])
    #  @commands.cooldown(1, 20, commands.BucketType.user)
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

    @commands.command(aliases=["mto", "weather"])
    #  @commands.cooldown(1, 20, commands.BucketType.user)
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

    @commands.command(aliases=["away", "idle"])
    async def afk(self, ctx):
        msg = ctx.message
        await msg.delete()

        user = ctx.message.author

        setting = await Settings().get_glob_settings()
        if 'AFK' not in setting:
            setting['AFK'] = []

        setting['AFK'].append(user.id)
        await Settings().set_glob_settings(setting)
        await ctx.send(f"{user.name}, you're now AFK !")

    async def on_message(self, message):
        author = message.author
        setting = await Settings().get_glob_settings()
        if 'AFK' in setting:
            if author.id in setting['AFK']:
                if message.content is '--afk':
                    return
                setting['AFK'].remove(author.id)
                await Settings().set_glob_settings(setting)
                await message.channel.send("{}, welcome back !".format(author.mention), delete_after=10)
            else:
                for user in message.mentions:
                    if user.id in setting['AFK']:
                        await message.channel.send("{}#{} is AFK".format(user.name, user.discriminator), delete_after=10)
                        await message.delete()
                        await author.send("{}#{} is AFK, this is your message : \n ```{}```".format(user.name, user.discriminator, message.content))


def setup(bot):
    bot.add_cog(General(bot, bot.config))
