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
import random

import discord
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
        self.hug = [
            "https://media1.tenor.com/images/506aa95bbb0a71351bcaa753eaa2a45c/tenor.gif",
            "https://media1.tenor.com/images/4d89d7f963b41a416ec8a55230dab31b/tenor.gif?itemid=5166500",
            "https://media1.tenor.com/images/dbd5f352c80e3445b801d548ca330a6a/tenor.gif?itemid=14214458",
            "https://media1.tenor.com/images/e58eb2794ff1a12315665c28d5bc3f5e/tenor.gif?itemid=10195705",
            "https://media1.tenor.com/images/074d69c5afcc89f3f879ca473e003af2/tenor.gif?itemid=4898650",
            "https://media1.tenor.com/images/45b1dd9eaace572a65a305807cfaec9f/tenor.gif?itemid=6238016",
            "https://media1.tenor.com/images/460c80d4423b0ba75ed9592b05599592/tenor.gif?itemid=5044460",
            "https://media1.tenor.com/images/b35c2462c7b623d050e28e6f1886a41f/tenor.gif?itemid=7419864",
            "https://media1.tenor.com/images/1a73e11ad8afd9b13c7f9f9bb5c9a834/tenor.gif?itemid=13366388",
            "https://media1.tenor.com/images/f2805f274471676c96aff2bc9fbedd70/tenor.gif?itemid=7552077",
            "https://media1.tenor.com/images/2d4138c7c24d21b9d17f66a54ee7ea03/tenor.gif?itemid=12535134",
            "https://media1.tenor.com/images/ff65c0f9b938f9594c822c6fc2690d4b/tenor.gif?itemid=16391919"
        ]
        self.pat = [
            "https://media1.tenor.com/images/116fe7ede5b7976920fac3bf8067d42b/tenor.gif?itemid=9200932",
            "https://media1.tenor.com/images/153e9bdd80008e8c0f94110450fcbf98/tenor.gif?itemid=10534102",
            "https://media1.tenor.com/images/b89e2aa380639d37b9521b72a266d498/tenor.gif?itemid=4215410",
            "https://media1.tenor.com/images/f5176d4c5cbb776e85af5dcc5eea59be/tenor.gif?itemid=5081286",
            "https://media1.tenor.com/images/0a35a0cc82d3b613086e0f420a94c2ad/tenor.gif?itemid=15779012",
            "https://media1.tenor.com/images/78421fd64eba6902f18a0574cce1b5f5/tenor.gif?itemid=14405998",
            "https://media1.tenor.com/images/9bf3e710f33cae1eed1962e7520f9cf3/tenor.gif?itemid=13236885",
            "https://media1.tenor.com/images/0feacf1898bd3223fa59a32c1c03d5ca/tenor.gif?itemid=12816949",
            "https://media1.tenor.com/images/5a692dc246f2468ca0e37446b4964054/tenor.gif?itemid=13949497",
            "https://media1.tenor.com/images/b7ddddf6d6da303dcdc3823959192b42/tenor.gif?itemid=15586999"
        ]

        self.kiss = [
            "https://media1.tenor.com/images/558f63303a303abfdddaa71dc7b3d6ae/tenor.gif?itemid=12879850",
            "https://media1.tenor.com/images/0ec5382910e34ca5649f6c328124daa1/tenor.gif?itemid=15556555",
            "https://media1.tenor.com/images/bc5e143ab33084961904240f431ca0b1/tenor.gif?itemid=9838409",
            "https://media1.tenor.com/images/a390476cc2773898ae75090429fb1d3b/tenor.gif?itemid=12837192",
            "https://media1.tenor.com/images/e76e640bbbd4161345f551bb42e6eb13/tenor.gif?itemid=4829336",
            "https://media1.tenor.com/images/1306732d3351afe642c9a7f6d46f548e/tenor.gif?itemid=6155670",
            "https://media1.tenor.com/images/f03f245e14fdfcacaf06318cdc667a03/tenor.gif?itemid=15111568",
            "https://media1.tenor.com/images/a1f7d43752168b3c1dbdfb925bda8a33/tenor.gif?itemid=10356314",
            "https://media1.tenor.com/images/7ea0b8822e5390c2393ef6f18a40893d/tenor.gif?itemid=16687888"
        ]

        self.lick = [
            "https://media1.tenor.com/images/ec2ca0bf12d7b1a30fea702b59e5a7fa/tenor.gif?itemid=13417195",
            "https://media1.tenor.com/images/5f73f2a7b302a3800b3613095f8a5c40/tenor.gif?itemid=10005495",
            "https://media1.tenor.com/images/feeef4685f9307b76c78a22ba0a69f48/tenor.gif?itemid=8413059"
        ]

        self.slap = [
            "https://media1.tenor.com/images/612e257ab87f30568a9449998d978a22/tenor.gif?itemid=16057834",
            "https://media1.tenor.com/images/3fd96f4dcba48de453f2ab3acd657b53/tenor.gif?itemid=14358509",
            "https://media1.tenor.com/images/d14969a21a96ec46f61770c50fccf24f/tenor.gif?itemid=5509136",
            "https://media1.tenor.com/images/0720ffb69ab479d3a00f2d4ac7e0510c/tenor.gif?itemid=10422113",
            "https://media1.tenor.com/images/4a6b15b8d111255c77da57c735c79b44/tenor.gif?itemid=10937039",
            "https://media1.tenor.com/images/5a348170ad2da23dc33fdf0f804bb609/tenor.gif?itemid=17100771",
            "https://media1.tenor.com/images/f9f121a46229ea904209a07cae362b3e/tenor.gif?itemid=7859254",
            "https://media1.tenor.com/images/71977e210574f341193b31a694b1a2eb/tenor.gif?itemid=15310661",
            "https://media1.tenor.com/images/153b2f1bfd3c595c920ce60f1553c5f7/tenor.gif?itemid=10936993",
            "https://media1.tenor.com/images/9ea4fb41d066737c0e3f2d626c13f230/tenor.gif?itemid=7355956",
            "https://media1.tenor.com/images/dcd359a74e32bca7197de46a58ec7b72/tenor.gif?itemid=12396060",
            "https://media1.tenor.com/images/7437caf9fb0bea289a5bb163b90163c7/tenor.gif?itemid=13595529"

        ]

        self.cry = [
            "https://media1.tenor.com/images/ce52606293142a2bd11cda1d3f0dc12c/tenor.gif?itemid=5184314",
            "https://media1.tenor.com/images/98466bf4ae57b70548f19863ca7ea2b4/tenor.gif?itemid=14682297",
            "https://media1.tenor.com/images/e69ebde3631408c200777ebe10f84367/tenor.gif?itemid=5081296",
            "https://media1.tenor.com/images/4b5e9867209d7b1712607958e01a80f1/tenor.gif?itemid=5298257",
            "https://media1.tenor.com/images/847d71cfe606022936e8acf2f09fb081/tenor.gif?itemid=12535132",
            "https://media1.tenor.com/images/09b085a6b0b33a9a9c8529a3d2ee1914/tenor.gif?itemid=5648908",
            "https://media1.tenor.com/images/0436bfc9861b4b57ffffda82d3adad6e/tenor.gif?itemid=15550145",
            "https://media1.tenor.com/images/dac529ebc72771b9d40373f0c4e10eff/tenor.gif?itemid=3532071",
            'https://media1.tenor.com/images/ecf674c5e0ed2fdf0260ade4fad2146f/tenor.gif?itemid=5580602'
        ]

    @commands.command()
    @commands.guild_only()
    async def hug(self, ctx, user: discord.Member = None):
        string = random.choice(self.hug)

        if not user:
            user = ctx.author
        em = await Embeds.format_social_embed(f"{ctx.author} hugs {user}", "hug", f"{string}",
                                              ctx.message)
        await ctx.send(embed=em)

    @commands.command()
    @commands.guild_only()
    async def pat(self, ctx, user: discord.Member = None):
        string = random.choice(self.pat)

        if not user:
            user = ctx.author
        em = await Embeds.format_social_embed(f"{ctx.author} pats {user}", "pat", f"{string}",
                                              ctx.message)
        await ctx.send(embed=em)

    @commands.command()
    @commands.guild_only()
    async def kiss(self, ctx, user: discord.Member = None):
        string = random.choice(self.kiss)

        if not user:
            user = ctx.author
        em = await Embeds.format_social_embed(f"{ctx.author} kisses {user}", "kiss", f"{string}",
                                              ctx.message)
        await ctx.send(embed=em)

    @commands.command()
    @commands.guild_only()
    async def lick(self, ctx, user: discord.Member = None):
        string = random.choice(self.lick)

        if not user:
            user = ctx.author
        em = await Embeds.format_social_embed(f"{ctx.author} licks {user}", "lick", f"{string}",
                                              ctx.message)
        await ctx.send(embed=em)

    @commands.command()
    @commands.guild_only()
    async def slap(self, ctx, user: discord.Member = None):
        string = random.choice(self.slap)

        if not user:
            user = ctx.author
        em = await Embeds.format_social_embed(f"{ctx.author} slaps {user}", "slap", f"{string}",
                                              ctx.message)
        await ctx.send(embed=em)

    @commands.command()
    @commands.guild_only()
    async def feed(self, ctx, user: discord.Member = None):
        string = random.choice(self.feed)

        if not user:
            user = ctx.author
        em = await Embeds.format_social_embed(f"{ctx.author} feeds {user}", "feed", f"{string}",
                                              ctx.message)
        await ctx.send(embed=em)

    @commands.command()
    @commands.guild_only()
    async def cry(self, ctx):
        string = random.choice(self.cry)

        em = await Embeds.format_social_embed(f"{ctx.author} cry", "cry", f"{string}",
                                              ctx.message)
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Social(bot))
