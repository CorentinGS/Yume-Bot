#  Copyright (c) 2020.
#  MIT License
#
#  Copyright (c) 2019 YumeNetwork
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import asyncio
import datetime
import random
import urllib.parse

import discord
import requests
from discord.ext import commands
from romme import RepublicanDate

from modules.utils import lists


class Fun(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.command(aliases=['8ball'])
    @commands.guild_only()
    async def eightball(self, ctx, *, question: str = None):
        """
        Ask to the 8Ball something
        """
        if question is None:
            await ctx.send('Oh shit! The crystal ball fell off.... Come back later')

        else:
            answer = random.choice(lists.ballresponse)
            await ctx.send(f"Question: {question}\nAnswer: {answer}")

    @commands.command(aliases=['chat'])
    @commands.guild_only()
    async def cat(self, ctx):
        """
        Nekos are life
        """
        r = requests.get('https://nekos.life/api/v2/img/meow')
        r = r.json()
        await ctx.send(r["url"])

    @commands.command()
    async def dog(self, ctx):
        """
        Doggy !!!
        """
        r = requests.get('https://random.dog/woof.json')
        r = r.json()
        await ctx.send(r["url"])

    @commands.command()
    @commands.guild_only()
    async def lovepower(self, ctx, user: discord.Member = None):
        """
        What's his love power
        """
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
        elif love == 69:
            emoji = "🔞"

        await ctx.send("Love power of {} is {}! {}".format(user.name, love, emoji))

    @commands.command()
    @commands.guild_only()
    async def rd(self, ctx):
        """
        Display the Republican Date
        """
        today = datetime.date.today()
        rd = RepublicanDate.from_gregorian(today.year, today.month, today.day)

        try:
            await ctx.send(rd)

        except discord.HTTPException:
            pass

    @commands.command()
    @commands.guild_only()
    async def choose(self, ctx, *, answers: str):
        """
        Random choice
        """
        toto = random.choice(answers.split())
        await ctx.send(toto)

    @commands.command()
    @commands.guild_only()
    async def linux(self, ctx):
        """
        Linux joke
        """
        answer = random.choice(lists.linux)
        embed = discord.Embed(colour=discord.Colour.green())
        embed.description = answer
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def number(self, ctx, number: int = None):
        """
        Teach you sth about a number
        """
        if not number:
            number = random.randrange(1, 1789)
        async with ctx.channel.typing():
            response = requests.get(f'http://numbersapi.com/{number}')
            response_year = requests.get(f'http://numbersapi.com/{number}/year')

            await ctx.send("**Number fact** :\n" + str(response.text) + "\n**Year fact** :\n" + str(response_year.text))

    @commands.command()
    async def trump(self, ctx, tag: str = None):
        """
        Trump is a meme
        """
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
        """
        Chuck Norris is GOD
        """
        async with ctx.channel.typing():
            r = requests.get("https://api.chucknorris.io/jokes/random")
            r = r.json()
            await ctx.send(r["value"])

    @commands.command(aliases=["dev_joke", "programmer_joke", "geekjoke"])
    @commands.guild_only()
    async def geek_joke(self, ctx):
        """
        If you're not a geek, go on your way
        """
        r = requests.get('https://geek-jokes.sameerkumar.website/api')
        await ctx.send(f"Geek Joke :\n**{r.text}**")

    @commands.command()
    @commands.guild_only()
    async def cookie(self, ctx, user: discord.Member):
        """
        Cookie Eater
        """
        await ctx.send(
            f"**{user.display_name}**, you've been given a cookie by **{ctx.author.display_name}**. :cookie:")

    @commands.command()
    @commands.guild_only()
    async def today(self, ctx):
        """
        Teach you sth about today
        """
        today = datetime.datetime.now()
        async with ctx.channel.typing():
            response = requests.get(f'http://numbersapi.com/{today.month}/{today.day}/date')
            await ctx.send(response.text)

    @commands.command(aliases=["ice-cream"])
    @commands.guild_only()
    async def ice(self, ctx, user: discord.Member):
        """
        Give an ice
        """
        await ctx.send(f"{user.mention}, here is your ice: :ice_cream:!")

    @commands.command(aliases=["l2g"])
    @commands.guild_only()
    async def lmgtfy(self, ctx, *, msg: str = None):
        """
        Let me google this for you
        """
        if not msg:
            url = "https://lmgtfy.com/?q=The+answer+to+life&p=1"
        else:
            url = f"http://lmgtfy.com/?q={urllib.parse.quote_plus(msg.lower().strip())}"
        await ctx.send(url)

    @commands.command(aliases=["love"])
    @commands.guild_only()
    async def love_calc(self, ctx, user: discord.Member, user_: discord.Member = None):
        """
        Can they date ?
        """
        if not user_:
            user_ = ctx.message.author
        random.seed(int(str(user.id) + str(user_.id)))

        if user == user_:
            if user.id == 282233191916634113:
                love = 0.0
            else:
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
        """
        Urban dic is you new best friend
        """
        async with ctx.channel.typing():
            url = requests.get(f'https://api.urbandictionary.com/v0/define?term={search}')
            url = url.json()

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

    @commands.command()
    @commands.guild_only()
    async def rps(self, ctx):
        embed1 = discord.Embed(
            title=f"Rock, Paper, Scissors",
            description="Please type the choice u want to use! \n \n[1] Rock \n \n[2] Paper \n \n[3] Scissors",
            colour=discord.Colour.dark_blue()
        )
        game = ["rock", "paper", "scissors"]
        results = ["You Won!", "You Lost!", "A Tie!"]
        bot = random.choice(game)
        await ctx.send(embed=embed1)
        try:
            msg = await self.bot.wait_for('message', timeout=120, check=lambda msg: msg.author == ctx.author)
        except asyncio.TimeoutError:
            await ctx.send('👎', delete_after=3)

        message = str(msg.content.lower())

        if message not in game and message not in ["1", "2", "3"]:
            await ctx.send("Please type a valid value! Was the spelling correct?")
            return

        if message == bot:
            result = results[2]
            colour = discord.Colour.blue()
        elif (message in ["paper", "2"] and bot == "rock") or (
                message in ["rock", "1"] and bot == "scissors") or (
                message in ["scissors", "3"] and bot == "paper"):
            result = results[0]
            colour = discord.Colour.green()
        else:
            result = results[1]
            colour = discord.Colour.dark_red()

        embed2 = discord.Embed(
            title=f"{ctx.message.author.display_name}'s Rock, Paper, Scissors Game!",
            description=f"Bot choice: `{bot.capitalize()}` \n \nYour choice:`{msg.content.capitalize()}` \n \nResult:`{result}`",
            colour=colour
        )
        await ctx.send(embed=embed2)


def setup(bot):
    bot.add_cog(Fun(bot))
