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

import json

import discord
from discord.ext import commands


class About(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.command()
    @commands.guild_only()
    async def about(self, ctx):
        """
        Gives information about the bot
        """

        with open('./config/config.json', 'r') as cjson:
            config = json.load(cjson)

        version = config["version"]
        owner_ = config["owner_id"]
        owner = await self.bot.fetch_user(owner_)

        total_users = len(self.bot.users)

        channels: int = 0
        for guild in self.bot.guilds:
            channels += len(guild.channels)

        site = '[Documentation](https://yumenetwork.net)'
        server = '[Discord](https://yumenetwork.net/yumebot/invite/)'
        lib = '[Discord.py](https://github.com/Rapptz/discord.py/tree/rewrite)'
        vote = '[Vote for me](https://top.gg/bot/456504213262827524)'

        embed = discord.Embed(
            title="About",
            colour=discord.Colour.dark_red(),
            url="www.yumenetwork.net"
        )
        embed.set_footer(text=f"YumeBot {version} | By {owner}",
                         icon_url=owner.avatar_url)

        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.url = 'https://yumenetwork.net'
        embed.add_field(name="Author", value="__Name__ : {}#{}\n __ID__: {}".format(
            owner.name, owner.discriminator, owner.id), inline=True)
        embed.add_field(
            name="Stats",
            value=f"__Guilds__ :{len(self.bot.guilds)}\n__Channels__: {channels} "
                  f"\n__Users__: {total_users}",
            inline=True)

        embed.add_field(
            name="Informations",
            value=f"__Version__ : {version} \n__Site__ : {site} \n__Support__ : {server} \n__Lib__ : {lib}\n__Vote__ : {vote}",
            inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(About(bot))
