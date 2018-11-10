from discord.ext import commands
import json

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


def setup(bot):
    bot.add_cog(Tags(bot))
