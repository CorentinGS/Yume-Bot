import discord
from discord.ext import commands
import json




class Help:

    conf = {}

    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

        global conf
        conf = config

    @commands.command(pass_context=True)
    @commands.guild_only()
    async def help(self, ctx):


        with open('./config/config.json', 'r') as cjson:
            config = json.load(cjson)

        prefix = config["prefix"]

        msg = ctx.message
        author = ctx.message.author
        embed = discord.Embed(
            set_author="Help Menu",
            color=discord.Colour.orange()
        )

        embed.add_field(name = "**General**", value= f"{prefix}help General")
        embed.add_field(name = "**Moderation**", value= f"{prefix}help Moderation")
        embed.add_field(name = "**Fun**", value= f"{prefix}help Fun")
        embed.add_field(name = "**Meteo**", value= f"{prefix}help Meteo")
        embed.add_field(name = "**Blacklist**", value= f"{prefix}help Blacklist")
        embed.add_field(name = "**Info**", value= f"{prefix}help Info")


        try:
            await msg.delete()
            return await author.send(embed=embed)

        except discord.HTTPException:
            pass


def setup(bot):
    bot.add_cog(Help(bot, bot.config))
