#  Copyright (c) 2019.
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

#
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#
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
