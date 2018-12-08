import discord
import random
from discord.ext import commands
from modules.utils import lists, http
import json
import datetime
import requests
import aiohttp


from romme import RepublicanDate

from bs4 import BeautifulSoup

with open('./config/keys.json', 'r') as cjson:
    keys = json.load(cjson)


class Fun:

    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    async def randomimageapi(self, ctx, url, endpoint):
        try:
            r = await http.get(url, res_method="json", no_cache=True)
        except json.JSONDecodeError:
            return await ctx.send("Couldn't find anything from the API")

        await ctx.send(r[endpoint])

    @commands.command(aliases=['8ball'])
    @commands.guild_only()
    async def eightball(self, ctx, *, question: str = None):
        await ctx.message.delete()

        if question is None:
            await ctx.send('Oh shit! The crystal ball fell off.... Come back later')

        else:
            answer = random.choice(lists.ballresponse)
            await ctx.send(f"Question: {question}\nAnswer: {answer}")

    @commands.command(aliases=['neko'])
    @commands.guild_only()
    async def cat(self, ctx):
        await ctx.message.delete()
        await self.randomimageapi(ctx, 'https://nekos.life/api/v2/img/meow', 'url')

    @commands.command(aliases=['Doggy'])
    @commands.guild_only()
    async def dog(self, ctx):
        await ctx.message.delete()
        await self.randomimageapi(ctx, 'https://random.dog/woof.json', 'url')

    @commands.command(aliases=['yt'])
    async def youtube(self, ctx, *, search: str):
        await ctx.message.delete()
        search = search.replace(' ', '+').lower()
        response = requests.get(
            f"https://www.youtube.com/results?search_query={search}").text
        result = BeautifulSoup(response, "lxml")
        dir_address = f"{result.find_all(attrs={'class': 'yt-uix-tile-link'})[0].get('href')}"
        output = f"**Top Result:**\nhttps://www.youtube.com{dir_address}"
        try:
            await ctx.send(output)
        except discord.Forbidden:
            return

    @commands.command()
    async def hug(self, ctx, user: discord.Member = None):
        await ctx.message.delete()
        if user is None:
            user = ctx.message.author
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.description = "Hug {}".format(user.mention)
        GIPHY_API_KEY = keys["giphy"]

        response = requests.get(
            f"http://api.giphy.com/v1/gifs/random?&api_key={GIPHY_API_KEY}&tag=hug").text

        data = json.loads(response)

        embed.set_image(url=data['data']['images']['original']['url'])

        await ctx.send(embed=embed)

    @commands.command()
    async def love(self, ctx, user: discord.Member = None):
        await ctx.message.delete()
        if user is None:
            user = ctx.message.author
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.description = "Hug {}".format(user.mention)
        GIPHY_API_KEY = keys["giphy"]

        response = requests.get(
            f"http://api.giphy.com/v1/gifs/random?&api_key={GIPHY_API_KEY}&tag=love").text

        data = json.loads(response)

        embed.set_image(url=data['data']['images']['original']['url'])

        await ctx.send(embed=embed)

    @commands.command()
    async def kiss(self, ctx, user: discord.Member = None):
        await ctx.message.delete()
        if user is None:
            user = ctx.message.author
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.description = "Hug {}".format(user.mention)
        GIPHY_API_KEY = keys["giphy"]

        response = requests.get(
            f"http://api.giphy.com/v1/gifs/random?&api_key={GIPHY_API_KEY}&tag=kiss").text

        data = json.loads(response)

        embed.set_image(url=data['data']['images']['original']['url'])

        await ctx.send(embed=embed)

    @commands.command()
    async def gif(self, ctx, arg: str = None):
        await ctx.message.delete()
        if arg is None:
            arg = "anime"
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.description = "{}".format(arg)
        GIPHY_API_KEY = keys["giphy"]

        response = requests.get(
            f"http://api.giphy.com/v1/gifs/random?&api_key={GIPHY_API_KEY}&tag={arg}").text

        data = json.loads(response)

        embed.set_image(url=data['data']['images']['original']['url'])

        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def lovepower(self, ctx, user: discord.Member = None):

        await ctx.message.delete()
        if user is None:
            user = ctx.message.author

        seed = user.discriminator

        random.seed(seed)
        love = random.randint(1, 100)

        if love < 20:
            emoji = "💔"
        elif love > 20:
            emoji = "❤"
        elif love > 50:
            emoji = '💖'
        elif love > 70:
            emoji = "💞"
        elif love > 99:
            emoji = "🖤"

        await ctx.send("Love power of {} is {}! {}".format(user.name, love, emoji))

    @commands.command()
    @commands.guild_only()
    async def rd(self, ctx):

        await ctx.message.delete()
        today = datetime.date.today()
        rd = RepublicanDate.from_gregorian(today.year, today.month, today.day)

        try:
            await ctx.send(rd)

        except discord.HTTPException:
            pass

    @commands.command(aliases=["god", 'yume'])
    async def king(self, ctx):

        await ctx.message.delete()

        answer = random.choice(lists.king)

        await ctx.send(f'{answer}')

    @commands.command(aliases=['poney', 'poneybleu', 'poneyrouge', 'poneyblanc', "poneyviolet", 'petitponey'])
    async def poneybleuetrougeetblancetviolet(self, ctx):
        await ctx.message.delete()

        answer = random.choice(lists.poney)

        await ctx.send(f'{answer}')


def setup(bot):
    bot.add_cog(Fun(bot))
