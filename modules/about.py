import discord
from discord.ext import commands
from modules.utils import checks
import json
from datetime import datetime
import os
import psutil


class About:

    conf = {}

    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.process = psutil.Process(os.getpid())



        global conf
        conf = config


    @commands.command(pass_context=True)
    @checks.is_owner()
    async def about(self, ctx):

        message = ctx.message
        await message.delete()

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
        embed.url = 'https://yumenetwork.gitbook.io/yumebot/'
        embed.add_field(name="Author", value="__Name__ : {}#{}\n __ID__: {}".format(owner.name, owner.discriminator, owner.id), inline=True)
        embed.add_field(name="Stats", value=f"__Guilds__ :{len(self.bot.guilds)}\n __Channels__ : {text} text & {voice} voice \n __Users__ : {total_users }", inline=True)
        embed.add_field(name="Informations", value=f"__Version__ : {VERSION} \n __Github__ : {github} \n __Site__ : {site} \n __Support__ : {server} \n __Lib__ : {lib}", inline=True)
        embed.add_field(name="RAM Usage", value=f"{ramUsage:.2f} MB", inline=False)
        embed.set_thumbnail(url=owner.avatar_url)

        return await ctx.send(embed=embed)


    @commands.command(pass_context=True)
    async def support(self, ctx):

        message = ctx.message
        await message.delete()

        embed = discord.Embed(title="Support", color=discord.Colour.red())

        embed.add_field(name="**Support**",
                        value="https://invite.gg/yumenetwork")
        embed.add_field(name="Documentation", value="https://yumenetwork.gitbook.io/yumebot/")
        embed.add_field(
            name="Github", value="https://github.com/yumenetwork/Yume-Bot")
        embed.add_field(name="Invite link", value="https://discordapp.com/api/oauth2/authorize?client_id=456504213262827524&permissions=8&redirect_uri=https%3A%2F%2Fgithub.com%2Fyumenetwork%2FYume-Bot&scope=bot")

        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(About(bot, bot.config))
