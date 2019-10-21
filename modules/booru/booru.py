from random import choice

import requests
from discord.ext import commands


class Booru(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.command(aliases=["yan"])
    @commands.is_nsfw()
    @commands.guild_only()
    async def yandere(self, ctx, tag: str = ""):
        url = requests.get(f"https://yande.re/post.json?limit=20&tags={tag}")
        url = url.json()
        try:
            image = choice(url)
        except IndexError:
            return await ctx.send("This tag doesn't exist... We couldn't find anything.")
        image_url = image['sample_url']

        await ctx.send(image_url)

    @yandere.error
    async def yandere_error(self, ctx, error):
        if isinstance(error, commands.NSFWChannelRequired):
            return


def setup(bot):
    bot.add_cog(Booru(bot))
