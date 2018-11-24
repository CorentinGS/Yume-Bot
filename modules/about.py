import discord
from discord.ext import commands

import json
import os
import psutil
import random

from modules.utils import checks, lists

class About:

    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config
        self.process = psutil.Process(os.getpid())

    @commands.command()
    @checks.is_owner()
    async def about(self, ctx):

        await ctx.message.delete()

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
        ramUsage = self.process.memory_full_info().rss / 1024**2

        embed = discord.Embed(
            title="About",
            colour=discord.Colour.dark_red()
        )
        em.set_footer(text=f'Tip: {tip}')
        embed.url = 'https://yumenetwork.gitbook.io/yumebot/'
        embed.add_field(name="Author", value="__Name__ : {}#{}\n __ID__: {}".format(
            owner.name, owner.discriminator, owner.id), inline=True)
        embed.add_field(
            name="Stats", value=f"__Guilds__ :{len(self.bot.guilds)}\n__Channels__ : {text} text & {voice} voice \n__Users__ : {total_users }", inline=True)
        embed.add_field(
            name="Informations", value=f"__Version__ : {VERSION} \n__Github__ : {github} \n__Site__ : {site} \n__Support__ : {server} \n__Lib__ : {lib}", inline=True)
        embed.add_field(name="RAM Usage",
                        value=f"{ramUsage:.2f} MB", inline=False)
        embed.set_thumbnail(url=owner.avatar_url)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(About(bot))
