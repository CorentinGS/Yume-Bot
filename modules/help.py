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
    async def help(self, ctx, *, arg : str = None):


        with open('./config/config.json', 'r') as cjson:
            config = json.load(cjson)

        prefix = config["prefix"]

        msg = ctx.message
        await msg.delete()
        author = ctx.message.author

        if arg is None:
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

                return await ctx.send(embed=embed)

            except discord.HTTPException:
                pass

        elif arg == 'general':
            embed = discord.Embed(
                set_author='General Help',
                color=discord.Colour.blue()
            )

            embed.add_field(name = "**Help**", value=f"{prefix}help")
            embed.add_field(name = "**Info**", value=f"{prefix}info (Server Informations)" )
            embed.add_field(name = "**Members**", value=f"{prefix}members (How many members ?)" )

            try:
                return await ctx.send(embed = embed)

            except discord.HTTPException:
                pass

        else:
            return await ctx.send("Invalid argument")




def setup(bot):
    bot.add_cog(Help(bot, bot.config))
