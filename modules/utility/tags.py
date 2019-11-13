import json

from discord.ext import commands

with open('modules/utils/tag.json', 'r') as cjson:
    tags = json.load(cjson)


class Tags(commands.Cog):
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

    @commands.group()
    async def tags(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.get)

    @tags.command()
    async def get(self, ctx):
        await ctx.message.delete()
        await ctx.send('[%s]' % ', '.join(map(str, tags)))

    @tags.command()
    async def suggest(self, ctx, name: str, *, value: str):
        return

    # TODO: Ajouter la possibilité de suggestion de tags avec validation dans le salon suggestion

def setup(bot):
    bot.add_cog(Tags(bot))
