import datetime
import json
import random
import urllib.parse

import discord
import requests
from discord.ext import commands
from romme import RepublicanDate

from modules.utils import http, lists


class Fun(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @staticmethod
    async def randomimageapi(ctx, url, endpoint):
        try:
            r = await http.get(url, res_method="json", no_cache=True)
        except json.JSONDecodeError:
            return await ctx.send("Couldn't find anything from the API")
        await ctx.send(r[endpoint])

    @commands.command(aliases=['8ball'])
    @commands.guild_only()
    async def eightball(self, ctx, *, question: str = None):
        """

        :param question: The question to be answered
        """
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

    @commands.command()
    async def dog(self, ctx):
        await ctx.message.delete()
        await self.randomimageapi(ctx, 'https://random.dog/woof.json', 'url')

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

    @commands.command()
    @commands.guild_only()
    async def choose(self, ctx, *, answers: str):
        toto = random.choice(answers.split())
        await ctx.send(toto)

    @commands.command()
    @commands.guild_only()
    async def number(self, ctx, number: int = None):
        if not number:
            number = random.randrange(1, 1789)
        async with ctx.channel.typing():
            response = requests.get(f'http://numbersapi.com/{number}')
            response_year = requests.get(f'http://numbersapi.com/{number}/year')

            await ctx.send("**Number fact** :\n" + str(response.text) + "\n**Year fact** :\n" + str(response_year.text))

    @commands.command()
    async def trump(self, ctx, tag: str = None):
        await ctx.message.delete()
        async with ctx.channel.typing():
            if not tag:
                response = requests.get("https://api.tronalddump.io/random/quote")
            else:
                response = requests.get(
                    f"https://api.tronalddump.io/tag/{urllib.parse.quote_plus(tag.lower().strip())}")
            r = response.json()
            await ctx.send(f"Geek Joke :\n**{r['value']}**")

    @commands.command(aliases=["chuck", "norris", "cn"])
    @commands.guild_only()
    async def chucknorris(self, ctx):
        await ctx.message.delete()
        async with ctx.channel.typing():
            r = requests.get("https://api.chucknorris.io/jokes/random")
            r = r.json()
            await ctx.send(r["value"])

    @commands.command(aliases=["dev_joke", "programmer_joke", "geekjoke"])
    @commands.guild_only()
    async def geek_joke(self, ctx):
        r = requests.get('https://geek-jokes.sameerkumar.website/api')
        await ctx.send(f"Geek Joke :\n**{r.text}**")

    @commands.command()
    @commands.guild_only()
    async def cookie(self, ctx, user: discord.Member):
        await ctx.send(
            f"**{user.display_name}**, you've been given a cookie by **{ctx.author.display_name}**. :cookie:")

    @commands.command()
    @commands.guild_only()
    async def today(self, ctx):
        today = datetime.datetime.now()
        async with ctx.channel.typing():
            response = requests.get(f'http://numbersapi.com/{today.month}/{today.day}/date')
            await ctx.send(response.text)

    @commands.command(aliases=["ice-cream"])
    @commands.guild_only()
    async def ice(self, ctx, user: discord.Member):
        await ctx.send(f"{user.mention}, here is your ice: :ice_cream:!")

    @commands.command(aliases=["l2g"])
    @commands.guild_only()
    async def lmgtfy(self, ctx, *, msg: str = None):
        if not msg:
            url = "https://lmgtfy.com/?q=The+answer+to+life&p=1"
        else:
            url = f"http://lmgtfy.com/?q={urllib.parse.quote_plus(msg.lower().strip())}"
        await ctx.send(url)
        await ctx.message.delete()

    @commands.command(aliases=["love"])
    @commands.guild_only()
    async def love_calc(self, ctx, user: discord.Member, user_: discord.Member = None):
        if not user_:
            user_ = ctx.message.author
        random.seed(int(str(user.id) + str(user_.id)))

        if user == user_:
            love = 100.00
        else:
            love = random.randint(1, 10000) / 100
        if love < 50:
            emoji = "💔"
        elif love > 50:
            emoji = '💖'
        elif love > 70:
            emoji = "💞"
        elif love > 99:
            emoji = "🖤"

        await ctx.send(f"{user.name} + {user_.name} = {emoji} | {love}% of love")

    @commands.command()
    @commands.guild_only()
    async def urban(self, ctx, *, search: str):
        async with ctx.channel.typing():
            url = await http.get(f'https://api.urbandictionary.com/v0/define?term={search}', res_method="json")

            if url is None:
                return await ctx.send("The API is broken...")

            if not len(url['list']):
                return await ctx.send("Couldn't find it...")

            result = sorted(url['list'], reverse=True, key=lambda g: int(g["thumbs_up"]))[0]

            definition = result['definition']
            if len(definition) >= 500:
                definition = definition[:500]
                definition = definition.rsplit(' ', 1)[0]
                definition += '...'

            await ctx.send(f"📚 Definitions for **{result['word']}**```fix\n{definition}```")


def setup(bot):
    bot.add_cog(Fun(bot))
