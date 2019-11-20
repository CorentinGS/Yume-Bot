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
        if ctx.invoked_subcommand is None:
            embed = await Embeds().format_commands_embed(ctx, self.bot.user.avatar_url)
            await ctx.send(embed=embed)

    @help.command()
    async def general(self, ctx):
        liste = "`jump`, `weather`, `gweather`, `afk`, `pokemon`, `anime`, `manga`, `character`, `anilist`"
        embed = await Embeds().format_cat_embed(ctx, self.bot.user.avatar_url, "General", liste)
        await ctx.send(embed=embed)

    @help.command()
    async def utils(self, ctx):
        liste = "`info`, `members`, `owner`, `date`, `whois`, `hackwhois`, " \
                "`avatar`, `icon`, `roleinfo`, `invite`, `channelinfo`, `tags`, `tag`"
        embed = await Embeds().format_cat_embed(ctx, self.bot.user.avatar_url, "Utils", liste)
        await ctx.send(embed=embed)

    @help.command()
    async def info(self, ctx):
        liste = "`about`, `help`, `suggestion`, `feedback`"
        embed = await Embeds().format_cat_embed(ctx, self.bot.user.avatar_url, "Info", liste)
        await ctx.send(embed=embed)

    @help.command()
    async def mods(self, ctx):
        liste = "`mute`, `unmute`, `ban`, `hackban`, `unban`, `kick`, `purge`, `sanction`," \
                " `strike`, `slowmode`, `deaf`, `undeaf`, `vmute`, `vunmute`, `nick`, `topic`"
        embed = await Embeds().format_cat_embed(ctx, self.bot.user.avatar_url, "Mods", liste)
        await ctx.send(embed=embed)

    @help.command()
    async def admin(self, ctx):
        liste = "`mention`, `annonce`, `massban`, `reset`, `addrole`, `fresh`, `poll`, `quickpoll`"
        embed = await Embeds().format_cat_embed(ctx, self.bot.user.avatar_url, "Admin", liste)
        await ctx.send(embed=embed)

    @help.command()
    async def level(self, ctx):
        liste = "`rank`, `level config`, `leaderboard`"
        embed = await Embeds().format_cat_embed(ctx, self.bot.user.avatar_url, "Level", liste)
        await ctx.send(embed=embed)

    @help.command()
    async def guild(self, ctx):
        liste = "`setting get`, `setting reset`, `setting setup`, `setting role mod`, `setting role admin`, `arr`, `setting color`, `color create`, `color list`, " \
                "`color add`, `color remove`"
        embed = await Embeds().format_cat_embed(ctx, self.bot.user.avatar_url, "Guild", liste)
        await ctx.send(embed=embed)

    @help.command()
    async def fun(self, ctx):
        liste = "`rd`, `8ball`, `cat`, `dog`, `lovepower`, `choose`, `linux`, `number`, `trump`, `chucknorris`, `geek_joke`, `cookie`, `today`," \
                " `ice`, `lmgtfy`, `love_calc`, `urban`"
        embed = await Embeds().format_cat_embed(ctx, self.bot.user.avatar_url, "Fun", liste)
        await ctx.send(embed=embed)

    @help.command()
    async def social(self, ctx):
        liste = "`hug`, `pat`, `kiss`, `lewd`, `lick`, `slap`, `cry`"
        embed = await Embeds().format_cat_embed(ctx, self.bot.user.avatar_url, "Social", liste)
        await ctx.send(embed=embed)

    @help.command()
    async def game(self, ctx):
        liste = "`truth`, `dare`, `wyr`, `nhie`"
        embed = await Embeds().format_cat_embed(ctx, self.bot.user.avatar_url, "Game", liste)
        await ctx.send(embed=embed)

    # TODO: Add owner commands


def setup(bot):
    bot.add_cog(Help(bot))
