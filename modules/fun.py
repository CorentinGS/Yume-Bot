import discord
import random
from discord.ext import commands
from modules.utils import lists, http
import json
import datetime
from romme import RepublicanDate


class Fun:

    conf = {}

    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

        global conf
        conf = config

    async def randomimageapi(self, ctx, url, endpoint):
        try:
            r = await http.get(url, res_method="json", no_cache=True)
        except json.JSONDecodeError:
            return await ctx.send("Couldn't find anything from the API")

        await ctx.send(r[endpoint])


    @commands.command(pass_context=True, aliases=['8ball'])
    @commands.guild_only()
    #@commands.cooldown(1, 3, commands.BucketType.user)
    async def eightball(self, ctx, *, question: str = None):

        if question is None:
            await ctx.send('Oh shit! The crystal ball fell off.... Come back later')
            return

        else:
            answer = random.choice(lists.ballresponse)
            return await ctx.send(f"Question: {question}\nAnswer: {answer}")

    @commands.command(pass_context=True, aliases=['neko'])
    @commands.guild_only()
    #@commands.cooldown(1, 3, commands.BucketType.guild)
    async def cat(self, ctx):
        return await self.randomimageapi(ctx, 'https://nekos.life/api/v2/img/meow', 'url')

    @commands.command(pass_context=True, aliases=['Doggy'])
    @commands.guild_only()
    #@commands.cooldown(1, 3, commands.BucketType.guild)
    async def dog(self, ctx):
        return await self.randomimageapi(ctx, 'https://random.dog/woof.json', 'url')

    @commands.command(pass_context=True)
    @commands.guild_only()
    #@commands.cooldown(1, 3, commands.BucketType.guild)
    async def lovepower(self, ctx, user: discord.Member = None):

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

    @commands.command(pass_context=True)
    @commands.guild_only()
    #@commands.cooldown(1, 60, commands.BucketType.user)
    async def rd(self, ctx):

        msg = ctx.message
        today = datetime.date.today()
        rd = RepublicanDate.from_gregorian(today.year, today.month, today.day)

        try:
            await ctx.send(rd)
            await msg.delete()
            return

        except discord.HTTPException:
            pass

    @commands.command(pass_context=True, aliases=["god", 'yume'])
    async def king(self, ctx):

        msg = ctx.message
        await msg.delete()

        answer = random.choice(lists.king)

        return await ctx.send(f'{answer}')

    @commands.command(pass_context=True, aliases=['poney', 'poneybleu', 'poneyrouge', 'poneyblanc', "poneyviolet", 'petitponey'])
    async def poneybleuetrougeetblancetviolet(self, ctx):
        msg = ctx.message
        await msg.delete()

        answer = random.choice(lists.poney)

        return await ctx.send(f'{answer}')


def setup(bot):
    bot.add_cog(Fun(bot, bot.config))
