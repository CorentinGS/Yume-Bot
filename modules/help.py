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

            embed.add_field(name = "**General**", value= f"{prefix}help general")
            embed.add_field(name = "**Blacklist**", value= f"{prefix}help blacklist")
            #embed.add_field(name = "**Moderation**", value= f"{prefix}help moderation")
            #embed.add_field(name = "**Fun**", value= f"{prefix}help fun")

            #embed.add_field(name = "**Blacklist**", value= f"{prefix}help blacklist")


            try:

                return await ctx.send(embed=embed)

            except discord.HTTPException:
                pass

        elif arg == 'general' or "General":
            embed = discord.Embed(
                set_author='General Help',
                color=discord.Colour.blue()
            )

            embed.add_field(name = "**Help**", value=f"{prefix}help")
            embed.add_field(name = "**Ping**", value=f"{prefix}ping")
            embed.add_field(name = "**FeedBack**", value=f"{prefix}feedback (send a feedback)")
            embed.add_field(name = "**Debug**", value=f"{prefix}debug (dm only)")
            embed.add_field(name = "**Weather**", value= f"{prefix}weather <city> (Display the weather)")


            try:
                return await ctx.send(embed = embed)

            except discord.HTTPException:
                pass


        elif arg == 'utils' or "Utils":
            embed = discord.Embed(
                set_author='Utils Help',
                color=discord.Colour.blue()
            )

            embed.add_field(name = "**Info**", value=f"{prefix}info (Server Informations)" )
            embed.add_field(name = "**Members**", value=f"{prefix}members (How many members ?)" )
            embed.add_field(name = "**Owner**", value=f"{prefix}owner (Display the Owner)" )

            try:
                return await ctx.send(embed = embed)

            except discord.HTTPException:
                pass

        elif arg == 'Blacklist' or "blacklist" or "bl":
            embed = discord.Embed(
                set_author='Blacklist Help',
                color=discord.Colour.blue()
            )

            embed.add_field(name = "**Blacklist**", value=f"{prefix}blacklist (Apply Blacklist !)" )
            embed.add_field(name = "**Soon**", value="Soon" )


            try:
                return await ctx.send(embed = embed)

            except discord.HTTPException:
                pass

        else:
            return await ctx.send("Invalid argument")




def setup(bot):
    bot.add_cog(Help(bot, bot.config))
