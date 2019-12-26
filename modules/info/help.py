#  Copyright (c) 2019.
#  MIT License
#
#  Copyright (c) 2019 YumeNetwork
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

#
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#
#
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#
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

    @staticmethod
    async def command_help(ctx, bot: discord.User, command: str, description: str, usage: str, example: str = None,
                           permission: str = None):
        embed = await Embeds().command_help(ctx, bot, command, description, usage, example, permission)
        await ctx.send(embed=embed)

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
    async def jump(self, ctx):
        await self.command_help(ctx, self.bot.user, "Jump", "Create a link to a message",
                                "--jump <message_id> [#channel]", "`--jump 645687761906434261 #general`")

    @help.command()
    async def meteo(self, ctx):
        await self.command_help(ctx, self.bot.user, "Weather", "Gives a city's weather forecast",
                                "--weather <city>",
                                "`--weather Paris`\n`--gweather Paris`")

    @help.command()
    async def afk(self, ctx):
        await self.command_help(ctx, self.bot.user, "Afk", "Set your profile to AFK", "--afk")

    @help.command()
    async def pokemon(self, ctx):
        await self.command_help(ctx, self.bot.user, "Pokemon", "Show pokemon info", "--pokemon <pokemon_name>",
                                "`--pokemon pikachu`")

    @help.command()
    async def anime(self, ctx):
        await self.command_help(ctx, self.bot.user, "Anime", "Shows information about an anime", "--anime <anime_name>",
                                "`--anime Naruto`")

    @help.command()
    async def manga(self, ctx):
        await self.command_help(ctx, self.bot.user, "Manga", "Shows information about a manga", "--manga <manga_name>",
                                "`--manga SAO`")

    @help.command()
    async def character(self, ctx):
        await self.command_help(ctx, self.bot.user, "Character", "Shows information about a manga/anime character",
                                "--character <character_name>",
                                "`--character Totoro`")

    @help.command()
    async def anilist(self, ctx):
        await self.command_help(ctx, self.bot.user, "Anilist", "Shows information about an anilist", "--anilist <user>",
                                "`--anilist yumenetwork`")

    @help.command()
    async def utils(self, ctx):
        liste = "`here`, `members`, `owner`, `age`, `whois`, `hackwhois`, " \
                "`avatar`, `icon`, `roleinfo`, `invite`, `channelinfo`, `tags`, `tag`"
        embed = await Embeds().format_cat_embed(ctx, self.bot.user.avatar_url, "Utils", liste)
        await ctx.send(embed=embed)

    @help.command()
    async def roleinfo(self, ctx):
        await self.command_help(ctx, self.bot.user, "RoleInfo", "Shows the information of a role", "--roleinfo <@role>",
                                "`--roleinfo @Member`")

    @help.command()
    async def channelinfo(self, ctx):
        await self.command_help(ctx, self.bot.user, "ChannelInfo", "Shows the information of a channel",
                                "--channelinfo <#channel>",
                                "`--channelinfo #general`")

    @help.command()
    async def invite(self, ctx):
        await self.command_help(ctx, self.bot.user, "Invite", "Gives a guild invitation", "--invite")

    @help.command()
    async def tags(self, ctx):
        await self.command_help(ctx, self.bot.user, "Tags", "Shows all tags", "--tags")

    @help.command()
    async def tag(self, ctx):
        await self.command_help(ctx, self.bot.user, "Tag", "Use a tag", "--tag <tag>", "`--tag vote`")

    @help.command()
    async def here(self, ctx):
        await self.command_help(ctx, self.bot.user, "Here", "Shows information about this guild", "--here")

    @help.command()
    async def members(self, ctx):
        await self.command_help(ctx, self.bot.user, "Members", "Shows members count", "--members")

    @help.command()
    async def owner(self, ctx):
        await self.command_help(ctx, self.bot.user, "Owner", "Shows the guild's owner", "--owner")

    @help.command()
    async def age(self, ctx):
        await self.command_help(ctx, self.bot.user, "Age", "Show the age of an account", "--age <@user>",
                                "`--age @YumeBot`")

    @help.command()
    async def whois(self, ctx):
        await self.command_help(ctx, self.bot.user, "Whois", "Show account information", "--whois <@user>",
                                "`--whois @YumeBot`")

    @help.command()
    async def hackwhois(self, ctx):
        await self.command_help(ctx, self.bot.user, "HackWhois", "Show account information using an id",
                                "--hackwhois <user_id>", "`--hackwhois 282233191916634113`")

    @help.command()
    async def avatar(self, ctx):
        await self.command_help(ctx, self.bot.user, "Avatar", "Steals a user's avatar", "--avatar <@user>",
                                "`--avatar @YumeBot`")

    @help.command()
    async def icon(self, ctx):
        await self.command_help(ctx, self.bot.user, "Icon", "Steals the guild's icon", "--icon")

    @help.command()
    async def info(self, ctx):
        liste = "`about`, `help`, `suggestion`, `feedback`"
        embed = await Embeds().format_cat_embed(ctx, self.bot.user.avatar_url, "Info", liste)
        await ctx.send(embed=embed)

    @help.command()
    async def about(self, ctx):
        await self.command_help(ctx, self.bot.user, "About", "Shows bot information", "--about")

    @help.command()
    async def suggestion(self, ctx):
        await self.command_help(ctx, self.bot.user, "Suggestion", "Create a suggestion post", "--suggestion")

    @help.command()
    async def feedback(self, ctx):
        await self.command_help(ctx, self.bot.user, "Feedback", "Create a feedback", "--feedback <text>",
                                "`--feedback Share this bot because it's an awesome one`")

    @help.command()
    async def mods(self, ctx):
        liste = "`mute`, `unmute`, `ban`, `hackban`, `unban`, `kick`, `purge`, `sanction`," \
                " `strike`, `slowmode`, `deaf`, `undeaf`, `vmute`, `vunmute`, `nick`, `topic`"
        embed = await Embeds().format_cat_embed(ctx, self.bot.user.avatar_url, "Mods", liste)
        await ctx.send(embed=embed)

    @help.command()
    async def mute(self, ctx):
        await self.command_help(ctx, self.bot.user, "Mute", "Mute an user", "--mute <user> <time> [reason]",
                                "`--mute @Yume 10m` - Mute Yume for 10 minutes")

    @help.command()
    async def unmute(self, ctx):
        await self.command_help(ctx, self.bot.user, "UnMute", "UnMute an user", "--mute <user> [reason]",
                                "`--unmute @Yume`")

    @help.command()
    async def ban(self, ctx):
        await self.command_help(ctx, self.bot.user, "Ban", "Ban an user", "--ban <user> [reason]",
                                "`--ban @Jack`")

    @help.command()
    async def hackban(self, ctx):
        await self.command_help(ctx, self.bot.user, "HackBan", "HackBan an user", "--ban <user_id> [reason]",
                                "`--hackban 282233191916634113`")

    @help.command()
    async def unban(self, ctx):
        await self.command_help(ctx, self.bot.user, "UnBan", "UnBan an user", "--unban <user_id>",
                                "`--unban 282233191916634113`")

    @help.command()
    async def kick(self, ctx):
        await self.command_help(ctx, self.bot.user, "Kick", "Kick an user", "--kick <user> [reason]",
                                "`--kick @Tux`")

    @help.command()
    async def purge(self, ctx):
        await self.command_help(ctx, self.bot.user, "Purge", "Purge the channel", "--purge <amount>",
                                "`--purge 100`")

    @help.command()
    async def sanction(self, ctx):
        await self.command_help(ctx, self.bot.user, "Sanction", "Provides information on a sanction report",
                                "--sanction <sanction_id>",
                                "`--sanction 20191225175936694142`")

    # TODO: Refaire une cmd de sanction séparé

    @help.command()
    async def sanctions(self, ctx):
        await self.command_help(ctx, self.bot.user, "Retrieves the list of sanctions of an user", "--sanctions <user>",
                                "`--sanction @Totoro`")

    @help.command()
    async def strike(self, ctx):
        await self.command_help(ctx, self.bot.user, "Strike someone", "--strike <user> [reason]",
                                "`--strike @Apple Stealing Information`")

    # TODO: Ajouter les dernières commandes de modération à la doc !

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
