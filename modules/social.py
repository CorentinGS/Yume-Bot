import discord
import requests
from discord.ext import commands

from modules.utils.format import Embeds


class Social(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.command()
    async def hug(self, ctx, user: discord.Member = None):
        await ctx.message.delete()
        if not user:
            user = ctx.author
        r = requests.get("https://rra.ram.moe/i/r?type=hug")
        r = r.json()
        em = await Embeds.format_social_embed(f"{ctx.author} hugs {user}", "hugs", f"https://rra.ram.moe{r['path']}",
                                              ctx.message)
        await ctx.send(embed=em)

    @commands.command()
    async def pat(self, ctx, user: discord.Member = None):
        await ctx.message.delete()
        if not user:
            user = ctx.author
        r = requests.get("https://rra.ram.moe/i/r?type=pat")
        r = r.json()
        em = await Embeds.format_social_embed(f"{ctx.author} pats {user}", "pats", f"https://rra.ram.moe{r['path']}",
                                              ctx.message)
        await ctx.send(embed=em)

    @commands.command()
    async def kiss(self, ctx, user: discord.Member = None):
        await ctx.message.delete()
        if not user:
            user = ctx.author
        r = requests.get("https://rra.ram.moe/i/r?type=kiss")
        r = r.json()
        em = await Embeds.format_social_embed(f"{ctx.author} kisses {user}", "kiss", f"https://rra.ram.moe{r['path']}",
                                              ctx.message)
        await ctx.send(embed=em)

    @commands.command()
    async def lick(self, ctx, user: discord.Member = None):
        await ctx.message.delete()
        if not user:
            user = ctx.author
        r = requests.get("https://rra.ram.moe/i/r?type=lick")
        r = r.json()
        em = await Embeds.format_social_embed(f"{ctx.author} licks {user}", "licks", f"https://rra.ram.moe{r['path']}",
                                              ctx.message)
        await ctx.send(embed=em)

    @commands.command()
    async def slap(self, ctx, user: discord.Member = None):
        await ctx.message.delete()
        if not user:
            user = ctx.author
        r = requests.get("https://rra.ram.moe/i/r?type=slap")
        r = r.json()
        em = await Embeds.format_social_embed(f"{ctx.author} slaps {user}", "slaps", f"https://rra.ram.moe{r['path']}",
                                              ctx.message)
        await ctx.send(embed=em)

    @commands.command()
    async def cry(self, ctx):
        await ctx.message.delete()
        r = requests.get("https://rra.ram.moe/i/r?type=cry")
        r = r.json()
        em = await Embeds.format_social_embed(f"{ctx.author} cry", "cry", f"https://rra.ram.moe{r['path']}",
                                              ctx.message)
        await ctx.send(embed=em)

    @commands.command()
    async def lewd(self, ctx):
        await ctx.message.delete()
        r = requests.get("https://rra.ram.moe/i/r?type=lewd")
        r = r.json()
        em = await Embeds.format_social_embed(f"{ctx.author} is lewd", "lewd", f"https://rra.ram.moe{r['path']}",
                                              ctx.message)
        await ctx.send(embed=em)

    @commands.command()
    async def slap(self, ctx, user: discord.Member = None):
        await ctx.message.delete()
        if not user:
            user = ctx.author
        r = requests.get("https://rra.ram.moe/i/r?type=slap")
        r = r.json()
        em = await Embeds.format_social_embed(f"{ctx.author} slaps {user}", "slaps", f"https://rra.ram.moe{r['path']}",
                                              ctx.message)
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Social(bot))
