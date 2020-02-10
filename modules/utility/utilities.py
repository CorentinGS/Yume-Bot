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


from datetime import datetime

import discord
from discord.ext import commands


class Utilities(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.command(aliases=["server"])
    @commands.guild_only()
    async def here(self, ctx):

        guild = ctx.message.guild

        if guild.mfa_level == 1:
            af = "True"
        else:
            af = "False"

        embed = discord.Embed(
            title="{}".format(ctx.message.guild.name),
            color=discord.Colour.dark_gold()
        )

        embed.set_footer(text=f"YumeBot",
                         icon_url=self.bot.user.avatar_url)

        embed.add_field(name="Name", value=guild.name, inline=True)
        embed.add_field(name="ID", value=guild.id, inline=True)
        embed.add_field(name="Roles", value=str(len(guild.roles)), inline=True)
        embed.add_field(name="Members", value=str(len(guild.members)), inline=True)
        embed.add_field(name="Channels", value=str(len(guild.channels)), inline=True)
        embed.add_field(name="Security",
                        value=guild.verification_level, inline=True)
        embed.add_field(name="Region", value=guild.region, inline=True)
        embed.add_field(name="Owner", value=guild.owner, inline=True)
        embed.add_field(name="2AF", value=af, inline=False)
        embed.add_field(name="created at", value=guild.created_at.strftime(
            '%A - %B - %e at %H:%M'), inline=False)
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(text=f"YumeBot",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(aliases=['ri'])
    @commands.guild_only()
    async def roleinfo(self, ctx, *, role: discord.Role):
        color = role.colour

        embed = discord.Embed(colour=color)

        embed.add_field(name="Users", value=str(len(role.members)))
        embed.add_field(name="Hoist", value=role.hoist)
        embed.add_field(name="Position", value=role.position)
        embed.add_field(name='Role ID', value=f'{role.id}')
        embed.add_field(name="Created", value=role.created_at)
        embed.set_footer(text=f"YumeBot",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @roleinfo.error
    async def roleinfo_error(self, ctx, error):
        if isinstance(error, commands.UserInputError):
            help = self.bot.get_cog('Help')
            await ctx.invoke(help.roleinfo)

    @commands.command(aliases=["ci"])
    @commands.guild_only()
    async def channelinfo(self, ctx, channel: discord.TextChannel = None):
        if not channel:
            channel = ctx.channel

        embed = discord.Embed(colour=discord.Colour.gold())

        embed.add_field(name="Channel Name", value=channel.name)
        embed.add_field(name="ID", value=channel.id)
        embed.add_field(name="Type", value=channel.type)
        embed.add_field(name="Created", value=channel.created_at)
        embed.add_field(name="Topic", value=channel.topic)
        embed.add_field(name='Nswf', value=channel.is_nsfw())

        embed.set_footer(text=f"YumeBot",
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @channelinfo.error
    async def chaninfo_error(self, ctx, error):
        if isinstance(error, commands.UserInputError):
            help = self.bot.get_cog('Help')
            await ctx.invoke(help.channelinfo)

    @commands.command()
    @commands.guild_only()
    async def members(self, ctx):
        """
        How many members do u have ?
        """
        onlines = 0
        bots = 0
        server = ctx.message.guild
        for member in server.members:
            if member.bot is True:
                bots += 1
            elif member.status != discord.Status.offline:
                onlines += 1

        embed = discord.Embed(
            title="{}".format(ctx.message.guild.name),
            color=discord.Colour.dark_gold()
        )

        embed.add_field(name="Members", value=str(len(server.members)))
        embed.add_field(name="Onlines", value=str(onlines))
        embed.add_field(name="Humans", value=str(len(server.members) - bots))
        embed.add_field(name="Bots", value=str(bots))

        embed.set_thumbnail(url=server.icon_url)
        embed.set_footer(text=f"YumeBot",
                         icon_url=self.bot.user.avatar_url)
        try:
            return await ctx.send(embed=embed)

        except discord.HTTPException:
            pass

    @commands.command()
    @commands.guild_only()
    async def owner(self, ctx):
        server = ctx.message.guild

        embed = discord.Embed(
            title="{}".format(ctx.message.guild.name),
            color=discord.Colour.dark_gold()
        )

        embed.add_field(name="Owner", value=server.owner.mention, inline=True)
        embed.set_thumbnail(url=server.owner.avatar_url)
        embed.set_footer(text=f"YumeBot",
                         icon_url=self.bot.user.avatar_url)

        try:
            await ctx.send(embed=embed)

        except discord.HTTPException:
            pass

    @commands.command()
    @commands.guild_only()
    async def age(self, ctx, member: discord.Member):
        """
        How old is he ?
        """
        now = datetime.now()
        create = member.created_at
        time = (now - create).days
        await ctx.send(f'**{member.name}** has created his account **{time}** days ago')

    @age.error
    async def age_error(self, ctx, error):
        if isinstance(error, commands.UserInputError):
            help = self.bot.get_cog('Help')
            await ctx.invoke(help.age)

    @commands.command()
    @commands.guild_only()
    async def avatar(self, ctx, *, user: discord.Member = None):
        """
        Avatar stealer
        """
        if user is None:
            user = ctx.author

        await ctx.send(f"Avatar of {user.name} \n {user.avatar_url_as(size=1024)}")

    @avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance(error, commands.UserInputError):
            help = self.bot.get_cog('Help')
            await ctx.invoke(help.avatar)

    @commands.command()
    @commands.guild_only()
    async def icon(self, ctx):
        """
        Icon stealer
        """
        await ctx.send(f"Icon of {ctx.guild.name}\n{ctx.guild.icon_url_as(size=1024)}")

    @commands.command(aliases=["userinfo", "ui"])
    @commands.guild_only()
    async def whois(self, ctx, user: discord.Member = None):
        """
        Who is he ?
        """
        if not user:
            user = ctx.author

        joins = sorted(ctx.guild.members, key=lambda o: o.joined_at)

        embed = discord.Embed(
            title="{}".format(user.name),
            color=discord.Colour.magenta()
        )
        embed.add_field(name="Nick", value=user.nick)
        embed.add_field(name="ID", value=user.id)
        embed.add_field(name="Status", value=user.status)
        embed.add_field(name="Hightest role", value=user.top_role)
        if user.activity:
            embed.add_field(name="Game Activity", value=user.activity.name)
        embed.add_field(name="Join position", value=str(joins.index(user)))
        embed.add_field(name="Created", value=user.created_at.strftime(
            '%A - %B - %e - %g at %H:%M'))
        embed.add_field(name="Joined", value=user.joined_at.strftime(
            '%A - %B - %e - %g at %H:%M'))

        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(text=f"YumeBot",
                         icon_url=self.bot.user.avatar_url)

        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            pass

    @whois.error
    async def whois_error(self, ctx, error):
        if isinstance(error, commands.UserInputError):
            help = self.bot.get_cog('Help')
            await ctx.invoke(help.whois)

    @commands.command()
    @commands.guild_only()
    async def hackwhois(self, ctx, id: int):
        """
        Who is this ID
        """

        user = await self.bot.fetch_user(id)

        embed = discord.Embed(
            title="{}".format(user.name),
            color=discord.Colour.magenta()
        )

        embed.add_field(name="Nick", value=user.nick)
        embed.add_field(name="ID", value=user.id)
        embed.add_field(name="Status", value=user.status)
        if user.activity:
            embed.add_field(name="Game Activity", value=user.activity.name)
        embed.add_field(name="Created", value=user.created_at.strftime(
            '%A - %B - %e - %g at %H:%M'))
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(text=f"YumeBot",
                         icon_url=self.bot.user.avatar_url)
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            pass

    @hackwhois.error
    async def hwhois_error(self, ctx, error):
        if isinstance(error, commands.UserInputError):
            help = self.bot.get_cog('Help')
            await ctx.invoke(help.hackwhois)

    @commands.command()
    @commands.guild_only()
    async def invite(self, ctx):
        """
        Create an invite
        """
        toto = await ctx.channel.create_invite(max_uses=15)
        await ctx.send(f"https://discord.gg/{toto.code}")


def setup(bot):
    bot.add_cog(Utilities(bot))
