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
            embed.add_field(name = "**About**", value=f"{prefix}help about")
            embed.add_field(name = "**Moderation**", value= f"{prefix}help mod")
            embed.add_field(name = "**Fun**", value= f"{prefix}help fun")
            embed.add_field(name= "**Administration**", value= f"{prefix}help admin")


            try:

                return await ctx.send(embed=embed)

            except discord.HTTPException:
                pass

        elif arg == 'general' or arg == "General":
            embed = discord.Embed(
                set_author='General Help',
                color=discord.Colour.blue()
            )

            embed.add_field(name = "**Help**", value=f"{prefix}help", inline = False)
            embed.add_field(name = "**Ping**", value=f"{prefix}ping", inline = False)
            embed.add_field(name = "**FeedBack**", value=f"{prefix}feedback (send a feedback)", inline = False)
            embed.add_field(name = "**Debug**", value=f"{prefix}debug (dm only)", inline = False)
            embed.add_field(name = "**Weather**", value= f"{prefix}weather <city> (Display the weather)", inline = False)
            embed.add_field(name = "**Global Weather", value= f"{prefix}gweather <gweather>", inline = False)


            try:
                return await ctx.send(embed = embed)

            except discord.HTTPException:
                pass

        elif arg == 'admin' or arg == "Admin" or arg == "administration":
            embed = discord.Embed(
                set_author='Admin Help',
                color=discord.Colour.blue()
            )

            embed.add_field(name = "**Mention**", value=f"{prefix}mention <role>", inline = False)
            embed.add_field(name = "**Annonce**", value=f"{prefix}annonce <role to mention> <message>", inline = False)


            try:
                return await ctx.send(embed = embed)

            except discord.HTTPException:
                pass

        elif arg == 'about' or arg == "About":
            embed = discord.Embed(
                set_author='About Help',
                color=discord.Colour.blue()
            )

            embed.add_field(name = "**About**", value=f"{prefix}about")
            embed.add_field(name = "**Credit**", value=f"{prefix}credit")
            embed.add_field(name = "**Lib**", value=f"{prefix}lib")


            try:
                return await ctx.send(embed = embed)

            except discord.HTTPException:
                pass

        elif arg == 'fun' or arg == "Fun":
            embed = discord.Embed(
                set_author='Fun Help',
                color=discord.Colour.blue()
            )

            embed.add_field(name = "**Republican Date**", value=f"{prefix}rd (display the republican date)", inline = False)
            embed.add_field(name = "**EightBall**", value=f"{prefix}8ball <question>", inline = False)
            embed.add_field(name = "**Cat**", value=f"{prefix}cat", inline = False)
            embed.add_field(name = "**Love Power**", value=f"{prefix}lovepower <user>", inline = False)


            try:
                return await ctx.send(embed = embed)

            except discord.HTTPException:
                pass

        elif arg == 'mod' or arg == "Mod":
            embed = discord.Embed(
                set_author='Mod Help',
                color=discord.Colour.blue()
            )

            embed.add_field(name = "**Mute**", value=f"{prefix}mute <mention> <time in m/h> <reason>(Mute an user)", inline = False)
            embed.add_field(name = "**Unmute**", value= f"{prefix}unmute <mention>", inline = False)
            embed.add_field(name = "**Kick**", value=f"{prefix}kick <mention> <reason>", inline = False)
            embed.add_field(name = "**Ban**", value=f"{prefix}ban <mention> <reason>", inline = False)
            embed.add_field(name = "**Hackban**", value=f"{prefix}hackban <id> <reason> (Prevent ban someone)", inline = False)
            embed.add_field(name = "**Unban**", value= f"{prefix}unban <id> (Unban Someone)", inline = False)
            embed.add_field(name = "**Massban**", value= f"{prefix}massban <reason> <ids> (Prevent Mass Ban)", inline = False)
            embed.add_field(name = "**Purge**", value= f"{prefix}purge <numbers> (Purge the chat)", inline = False)


            try:
                return await ctx.send(embed = embed)

            except discord.HTTPException:
                pass


        elif arg == 'utils' or arg == "Utils":
            embed = discord.Embed(
                set_author='Utils Help',
                color=discord.Colour.blue()
            )

            embed.add_field(name = "**Info**", value=f"{prefix}info (Server Informations)", inline = False)
            embed.add_field(name = "**Members**", value=f"{prefix}members (How many members ?)", inline = False )
            embed.add_field(name = "**Owner**", value=f"{prefix}owner (Display the Owner)", inline = False )
            embed.add_field(name = "**whois**", vaue= f"{prefix}whois <mention> (User Informations from Guild)", inline = False)
            embed.add_field(name = "**Hackwhois**", value= f"{prefix}hackwhois <id> (User Informations from ID)", inline = False)
            embed.add_field(name = "**Awatar**", value= f"{prefix}avatar <mention> (Get an avatar)", inline = False)
            embed.add_field(name = "**Guild Icon**", value= f"{prefix}icon (Get the icon)", inline = False)

            try:
                return await ctx.send(embed = embed)

            except discord.HTTPException:
                pass

        elif arg == 'Blacklist' or arg == "blacklist" or arg == "bl":
            embed = discord.Embed(
                set_author='Blacklist Help',
                color=discord.Colour.blue()
            )

            embed.add_field(name = "**Blacklist**", value=f"{prefix}blacklist (Apply Blacklist !)", inline = False)
            embed.add_field(name = "**Soon**", value="Soon" )


            try:
                return await ctx.send(embed = embed)

            except discord.HTTPException:
                pass

        else:
            return await ctx.send("Invalid argument")




def setup(bot):
    bot.add_cog(Help(bot, bot.config))
