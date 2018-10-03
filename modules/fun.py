import discord
import random
from discord.ext import commands
from modules.utils import lists, http


class Fun:

    conf = {}

    def __init__(self, client, config):
        self.client = client
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
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def eightball(self, ctx, *, question: str = None):

        if question is None:
            await ctx.send('Oh shit! The crystal ball fell off.... Come back later')
            return

        else:
            answer = random.choice(lists.ballresponse)
            return await ctx.send(f"Question: {question}\nAnswer: {answer}")

    @commands.command(pass_context=True, aliases=['neko'])
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.guild)
    async def cat(self, ctx):
        await self.randomimageapi(ctx, 'https://nekos.life/api/v2/img/meow', 'url')

    @commands.command(pass_context=True)
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.guild)
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


def setup(client):
    client.add_cog(Fun(client, client.config))
