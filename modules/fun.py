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


    @commands.command(pass_context = True, aliases=['8ball'])
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def eightball(self, ctx, *, question: str = None):

        if question is None:
            await ctx.send('Oh shit! The crystal ball fell off.... Come back later')
            return

        else:
            answer = random.choice(lists.ballresponse)
            return await ctx.send(f"Question: {question}\nAnswer: {answer}")



    @commands.command(pass_context = True, aliases=['neko'])
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def cat(self, ctx):
        await self.randomimageapi(ctx, 'https://nekos.life/api/v2/img/meow', 'url')


    @commands.command(pass_context = True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def love(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.message.author

        random.seed(user.id)
        r = random.randint(1, 100)
        love = r / 1.6

        if love < 20:
            emoji = "💔"
        elif live > 20:
            emoji = "❤"
        elif love > 50:
            emoji = '💖'
        elif love > 70:
            emoji = "💞"
        elif love > 99:
            emoji = "🖤"

        return await ctx.send(f"Love power of {user.name} is {love:.2f}! {emoji}")



def setup(client):
    client.add_cog(Fun(client, client.config))
