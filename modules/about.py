import json
import os
import random
import aiohttp


import discord
from discord.ext import commands

from modules.utils import checks, lists


class About(commands.Cog):

    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.command()
    async def req(self, ctx):
        url = "http://localhost:8080/people/4"

        async with aiohttp.ClientSession() as cs:
            async with cs.post(url, data= ({"firstname": "Toto",
                  "lastname": "Yume",
                    "address": { 
                        "city": "Nice",   
                        "state": "06"  }
                        })) as r:

                toto = await r.text()
                await ctx.send(toto)


    @commands.command()
    async def about(self, ctx):

        await ctx.message.delete()
        tip = random.choice(lists.tip)

        with open('./config/config.json', 'r') as cjson:
            config = json.load(cjson)

        VERSION = config["version"]
        OWNER = config["owner_id"]
        owner = await self.bot.get_user_info(OWNER)

        total_users = len(self.bot.users)

        voice_channels = []
        text_channels = []
        for guild in self.bot.guilds:
            voice_channels.extend(guild.voice_channels)
            text_channels.extend(guild.text_channels)

        text = len(text_channels)
        voice = len(voice_channels)

        github = '[Sources](https://github.com/yumenetwork/Yume-Bot)'
        site = '[Documentation](https://yumenetwork.gitbook.io/yumebot/)'
        server = '[Discord](https://invite.gg/yumenetwork)'
        lib = '[Discord.py](https://github.com/Rapptz/discord.py/tree/rewrite)'

        embed = discord.Embed(
            title="About",
            colour=discord.Colour.dark_red()
        )
        embed.set_footer(text=f'Tip: {tip}')
        embed.url = 'https://yumenetwork.gitbook.io/yumebot/'
        embed.add_field(name="Author", value="__Name__ : {}#{}\n __ID__: {}".format(
            owner.name, owner.discriminator, owner.id), inline=True)
        embed.add_field(
            name="Stats", value=f"__Guilds__ :{len(self.bot.guilds)}\n__Channels__ : {text} text & {voice} voice \n__Users__ : {total_users }", inline=True)
        embed.add_field(
            name="Informations", value=f"__Version__ : {VERSION} \n__Github__ : {github} \n__Site__ : {site} \n__Support__ : {server} \n__Lib__ : {lib}", inline=True)

        embed.set_thumbnail(url=owner.avatar_url)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(About(bot))
