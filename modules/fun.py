import datetime
import json
import random

import discord
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
    async def urban(self, ctx, *, search:str):
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


    '''
    @commands.command()
    @commands.guild_only()
    async def marry(self, ctx, user: discord.Member =  None):

        def check(reaction, toto):
            return toto == user and str(reaction.emoji)

        reactions = ["👍", "🖕"]

        await ctx.message.delete()
        if user is None:
            await ctx.send("Hey you can't get married alone... retry")

        else:
            msg = await ctx.send("Hey {}, {} wants to marry you.\n Do you agree ?".format(user.name, ctx.message.author.name))
            for reac in reactions:
             await msg.add_reaction(reac)

        reaction, toto = await self.bot.wait_for('reaction_add', timeout=120, check=check)
        '''

def setup(bot):
    bot.add_cog(Fun(bot))
