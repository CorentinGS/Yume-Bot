import json

import discord
from discord.ext import commands


class About(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.command()
    async def about(self, ctx):
        await ctx.message.delete()

        with open('./config/config.json', 'r') as cjson:
            config = json.load(cjson)

        version = config["version"]
        owner_ = config["owner_id"]
        owner = await self.bot.fetch_user(owner_)

        total_users = len(self.bot.users)

        voice_channels = []
        text_channels = []
        for guild in self.bot.guilds:
            voice_channels.extend(guild.voice_channels)
            text_channels.extend(guild.text_channels)

        text = len(text_channels)
        voice = len(voice_channels)

        site = '[Documentation](https://yumenetwork.gitbook.io/yumebot/)'
        server = '[Discord](https://invite.gg/yumenetwork)'
        lib = '[Discord.py](https://github.com/Rapptz/discord.py/tree/rewrite)'

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
            value=f"__Guilds__ :{len(self.bot.guilds)}\n__Channels__: {text}text & {voice}voice "
                  f"\n__Users__: {total_users}",
            inline=True)

        embed.add_field(
            name="Informations",
            value=f"__Version__ : {version} \n__Site__ : {site} \n__Support__ : {server} \n__Lib__ : {lib}",
            inline=True)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(About(bot))
