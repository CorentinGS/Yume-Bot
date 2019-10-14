import discord
from discord.ext import commands

from modules.utils.format import Embeds


class Help(commands.Cog):

    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.command()
    async def bot(self, ctx):
        await ctx.send(f"**{ctx.author.name}**, this is my URL: \n<{discord.utils.oauth_url(self.bot.user.id)}>")

    @commands.group(aliases=["c", "commands", "h"])
    async def help(self, ctx):
        embed = await Embeds().format_commands_embed(ctx, self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @help.command()
    async def general(self, ctx):
        liste = "`jump`, `debug`, `weather`, `gweather`, `afk`"
        embed = await Embeds().format_cat_embed(ctx, self.bot.user.avatar_url, "General", liste)
        await ctx.send(embed=embed)

    @help.command()
    async def utils(self, ctx):
        liste = "`info`, `members`, `owner`, `date`, `whois`, `hackwhois`, " \
                "`avatar`, `icon`, `roleinfo`, `invite`, `channelinfo`"
        embed = await Embeds().format_cat_embed(ctx, self.bot.user.avatar_url, "Utils", liste)
        await ctx.send(embed=embed)

    @help.command()
    async def about(self, ctx):
        liste = "`about`, `help`, `suggestion`, `feedback`"
        embed = await Embeds().format_cat_embed(ctx, self.bot.user.avatar_url, "About", liste)
        await ctx.send(embed=embed)

    @help.command()
    async def mods(self, ctx):
        liste = "`mute`, `unmute`, `ban`, `hackban`, `unban`, `kick`, `purge`, `sanction`," \
                " `strike`, `slowmode`, `deaf`, `undeaf`, `vmute`, `vunmute`, `nick`, `topic`"
        embed = await Embeds().format_cat_embed(ctx, self.bot.user.avatar_url, "Mods", liste)
        await ctx.send(embed=embed)

    @help.command()
    async def admin(self, ctx):
        liste = "`mention`, `annonce`, `massban`, `reset`"
        embed = await Embeds().format_cat_embed(ctx, self.bot.user.avatar_url, "Admin", liste)
        await ctx.send(embed=embed)

    @help.command()
    async def level(self, ctx):
        liste = "`rank`, `level config`"
        embed = await Embeds().format_cat_embed(ctx, self.bot.user.avatar_url, "Level", liste)
        await ctx.send(embed=embed)

    @help.command()
    async def settings(self, ctx):
        liste = "`settings get`, `settings reset`, `settings setup`, `settings role mod`, `settings role admin`"
        embed = await Embeds().format_cat_embed(ctx, self.bot.user.avatar_url, "Settings", liste)
        await ctx.send(embed=embed)

    @help.command()
    async def fun(self, ctx):
        liste = "`rd`, `8ball`, `cat`, `dog`, `lovepower`, `choose`, `number`, `trump`, `chucknorris`, `geek_joke`, `cookie`, `today`," \
                " `ice`, `lmgtfy`, `love_calc`, `urban`"
        embed = await Embeds().format_cat_embed(ctx, self.bot.user.avatar_url, "Fun", liste)
        await ctx.send(embed=embed)

    @help.command()
    async def social(self, ctx):
        liste = "`hug`, `pat`, `kiss`, `lewd`, `lick`, `slap`, `cry`"
        embed = await Embeds().format_cat_embed(ctx, self.bot.user.avatar_url, "social", liste)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))
