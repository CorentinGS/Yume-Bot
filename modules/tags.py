import json

from discord.ext import commands

with open('modules/utils/tag.json', 'r') as cjson:
    tags = json.load(cjson)


class Tags:
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.command()
    async def tag(self, ctx, *, name: str = None):
        await ctx.message.delete()

        if name in tags:
            await ctx.send(f"{tags[str(name)]}")
        else:
            await ctx.send("Unknown tag")

    @commands.command()
    async def tags(self, ctx):
        await ctx.message.delete()

        await ctx.send('[%s]' % ', '.join(map(str, tags)))



def setup(bot):
    bot.add_cog(Tags(bot))
