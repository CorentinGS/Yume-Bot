import discord
from discord.ext import commands
import json
from .utils.search import duckduckgo, qwant, discordpy, youtube, stack


class Shortcut:

    conf = {}

    def __init__(self, client, config):
        self.client = client
        self.config = config

        global conf
        conf = config

    @commands.command(pass_context=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ddg(self, ctx, *, content: str):

        msg = ctx.message
        result = duckduckgo(content)

        if len(content) < 1:
            return await ctx.send("What are u looking for ? Tell me more, tell me more !!!")

        else:
            try:
                await msg.delete()
                return await ctx.send("This is your result  : **{}**" .format(result))

            except:
                pass

    @commands.command(pass_context=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def qwant(self, ctx, *, content: str):

        msg = ctx.message
        result = qwant(content)

        if len(content) < 1:
            return await ctx.send("What are u looking for ? Tell me more, tell me more !!!")

        else:
            try:
                await msg.delete()
                return await ctx.send("This is your result  : **{}**" .format(result))

            except:
                pass

    @commands.command(pass_context=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def discordpy(self, ctx, *, content: str):

        msg = ctx.message
        result = discordpy(content)

        if len(content) < 1:
            return await ctx.send("What are u looking for ? Tell me more, tell me more !!!")

        else:
            try:
                await msg.delete()
                return await ctx.send("This is your result  : **{}**" .format(result))

            except:
                pass

    @commands.command(pass_context=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def youtube(self, ctx, *, content: str):

        msg = ctx.message
        result = youtube(content)

        if len(content) < 1:
            return await ctx.send("What are u looking for ? Tell me more, tell me more !!!")

        else:
            try:
                await msg.delete()
                return await ctx.send("This is your result  : **{}**" .format(result))

            except:
                pass

    @commands.command(pass_context=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def stack(self, ctx, *, content: str):

        msg = ctx.message
        result = stack(content)

        if len(content) < 1:
            return await ctx.send("What are u looking for ? Tell me more, tell me more !!!")

        else:
            try:
                await msg.delete()
                return await ctx.send("This is your result  : **{}**" .format(result))

            except:
                pass


'''
    @commands.command(pass_context = True)
    @commands.cooldown(2, 20, commands.BucketType.user)
    async def helloworld(self, ctx, *, content: str):

        msg = ctx.message
        author = ctx.message.author


        embed = discord.Embed(
            title="Hello World",
            color = discord.Colour.dark_red()
        )

        embed.add_field(name="{}".format(author), value="{}".format(content), inline=True)

        await msg.delete()
        return await ctx.send(embed)
'''

# TODO: Add more shortcut on the same model (using utils/search.py)


def setup(client):
    client.add_cog(Shortcut(client, client.config))
