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
import random

import discord
import requests
from discord.ext import commands

from modules.utils.format import Embeds


class Social(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config
        self.feed = [
            "https://media1.tenor.com/images/93c4833dbcfd5be9401afbda220066ee/tenor.gif?itemid=11223742",
            "https://media1.tenor.com/images/33cfd292d4ef5e2dc533ff73a102c2e6/tenor.gif?itemid=12165913",
            "https://media1.tenor.com/images/72268391ffde3cd976a456ee2a033f46/tenor.gif?itemid=7589062",
            "https://media1.tenor.com/images/4b48975ec500f8326c5db6b178a91a3a/tenor.gif?itemid=12593977",
            "https://media1.tenor.com/images/187ff5bc3a5628b6906935232898c200/tenor.gif?itemid=9340097",
            "https://media1.tenor.com/images/15e7d9e1eb0aad2852fabda1210aee95/tenor.gif?itemid=12005286",
            "https://media1.tenor.com/images/d08d0825019c321f21293c35df8ed6a9/tenor.gif?itemid=9032297",
            "https://media1.tenor.com/images/571da4da1ad526afe744423f7581a452/tenor.gif?itemid=11658244",
            "https://media1.tenor.com/images/6bde17caa5743a22686e5f7b6e3e23b4/tenor.gif?itemid=13726430",
            "https://media1.tenor.com/images/fd3616d34ade61e1ac5cd0975c25a917/tenor.gif?itemid=13653906",
            "https://imgur.com/v7jsPrv",
        ]

    @commands.command()
    async def hug(self, ctx, user: discord.Member = None):
        if not user:
            user = ctx.author
        r = requests.get("https://rra.ram.moe/i/r?type=hug")
        r = r.json()
        em = await Embeds.format_social_embed(f"{ctx.author} hugs {user}", "hug", f"https://rra.ram.moe{r['path']}",
                                              ctx.message)
        await ctx.send(embed=em)

    @commands.command()
    async def pat(self, ctx, user: discord.Member = None):
        if not user:
            user = ctx.author
        r = requests.get("https://rra.ram.moe/i/r?type=pat")
        r = r.json()
        em = await Embeds.format_social_embed(f"{ctx.author} pats {user}", "pat", f"https://rra.ram.moe{r['path']}",
                                              ctx.message)
        await ctx.send(embed=em)

    @commands.command()
    async def kiss(self, ctx, user: discord.Member = None):
        if not user:
            user = ctx.author
        r = requests.get("https://rra.ram.moe/i/r?type=kiss")
        r = r.json()
        em = await Embeds.format_social_embed(f"{ctx.author} kisses {user}", "kiss", f"https://rra.ram.moe{r['path']}",
                                              ctx.message)
        await ctx.send(embed=em)

    @commands.command()
    async def lick(self, ctx, user: discord.Member = None):
        if not user:
            user = ctx.author
        r = requests.get("https://rra.ram.moe/i/r?type=lick")
        r = r.json()
        em = await Embeds.format_social_embed(f"{ctx.author} licks {user}", "lick", f"https://rra.ram.moe{r['path']}",
                                              ctx.message)
        await ctx.send(embed=em)

    @commands.command()
    async def slap(self, ctx, user: discord.Member = None):
        if not user:
            user = ctx.author
        r = requests.get("https://rra.ram.moe/i/r?type=slap")
        r = r.json()
        em = await Embeds.format_social_embed(f"{ctx.author} slaps {user}", "slap", f"https://rra.ram.moe{r['path']}",
                                              ctx.message)
        await ctx.send(embed=em)

    @commands.command()
    async def feed(self, ctx, user: discord.Member = None):
        string = random.choice(self.feed)

        if not user:
            user = ctx.author
        em = await Embeds.format_social_embed(f"{ctx.author} feeds {user}", "feed", f"{string}",
                                              ctx.message)
        await ctx.send(embed=em)


    @commands.command()
    async def cry(self, ctx):
        r = requests.get("https://rra.ram.moe/i/r?type=cry")
        r = r.json()
        em = await Embeds.format_social_embed(f"{ctx.author} cry", "cry", f"https://rra.ram.moe{r['path']}",
                                              ctx.message)
        await ctx.send(embed=em)

    @commands.command()
    async def lewd(self, ctx):
        r = requests.get("https://rra.ram.moe/i/r?type=lewd")
        r = r.json()
        em = await Embeds.format_social_embed(f"{ctx.author} is lewd", "lewd", f"https://rra.ram.moe{r['path']}",
                                              ctx.message)
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Social(bot))
