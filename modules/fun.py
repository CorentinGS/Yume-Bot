import datetime
import json
import random

import discord
from discord.ext import commands
from romme import RepublicanDate

from modules.utils import http, lists

with open('./config/keys.json', 'r') as cjson:
    keys = json.load(cjson)


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


def setup(bot):
    bot.add_cog(Fun(bot))
