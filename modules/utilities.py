import random
from datetime import datetime

import discord
from discord.ext import commands

from modules.utils import lists

tip = random.choice(lists.tip)


class Utilities(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.command(aliases=["server"])
    @commands.guild_only()
    async def info(self, ctx):
        await ctx.message.delete()

        server = ctx.message.guild

        if server.mfa_level == 1:
            af = "True"

        else:
            af = "False"

        embed = discord.Embed(
            title="{}".format(ctx.message.guild.name),
            description="I found this...",
            color=discord.Colour.dark_gold()
        )
        embed.set_footer(text=f'Tip: {tip}')

        embed.add_field(name="Name", value=server.name, inline=True)
        embed.add_field(name="ID", value=server.id, inline=True)
        embed.add_field(name="Roles", value=str(len(server.roles)), inline=True)
        embed.add_field(name="Members", value=str(len(server.members)), inline=True)
        embed.add_field(name="Channels", value=str(len(server.channels)), inline=True)
        embed.add_field(name="Security",
                        value=server.verification_level, inline=True)
        embed.add_field(name="Region", value=server.region, inline=True)
        embed.add_field(name="Owner", value=server.owner, inline=True)
        embed.add_field(name="2AF", value=af, inline=False)
        embed.add_field(name="created at", value=server.created_at.strftime(
            '%A - %B - %e at %H:%M'), inline=False)
        embed.set_thumbnail(url=server.icon_url)

        try:
            await ctx.send(embed=embed)

        except discord.HTTPException:
            pass

    @commands.command(aliases=['ri'])
    @commands.guild_only()
    async def roleinfo(self, ctx, *, role: discord.Role):
        color = role.colour

        embed = discord.Embed(colour=color)

        embed.add_field(name="Users", value=str(len(role.members)))
        embed.add_field(name="Hoist", value=role.hoist)
        embed.add_field(name="Position", value=role.position)
        embed.add_field(name='Role ID', value=f'{role.id}')

        await ctx.send(embed=embed)

    @commands.command(aliases=["ci"])
    @commands.guild_only()
    async def channelinfo(self, ctx, channel: discord.TextChannel= None):
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

    @commands.command()
    @commands.guild_only()
    async def members(self, ctx):
        await ctx.message.delete()

        server = ctx.message.guild

        embed = discord.Embed(
            title="{}".format(ctx.message.guild.name),
            description="I found this...",
            color=discord.Colour.dark_gold()
        )

        embed.add_field(name="Members", value=str(len(server.members)), inline=True)
        embed.set_thumbnail(url=server.icon_url)

        try:
            return await ctx.send(embed=embed)

        except discord.HTTPException:
            pass

    @commands.command()
    @commands.guild_only()
    async def owner(self, ctx):
        await ctx.message.delete()
        server = ctx.message.guild

        embed = discord.Embed(
            title="{}".format(ctx.message.guild.name),
            description="I found this...",
            color=discord.Colour.dark_gold()
        )

        embed.add_field(name="Owner", value=server.owner.mention, inline=True)
        embed.set_thumbnail(url=server.icon_url)

        try:
            await ctx.send(embed=embed)

        except discord.HTTPException:
            pass

    @commands.command()
    @commands.guild_only()
    async def date(self, ctx, member: discord.Member):
        now = datetime.now()
        create = member.created_at
        time = (now - create).days
        await ctx.send(f'**{member.name}** has created his account **{time}** days ago')

    @commands.command()
    @commands.guild_only()
    async def avatar(self, ctx, *, user: discord.Member = None):

        if user is None:
            user = ctx.author

        await ctx.send(f"Avatar of {user.name} \n {user.avatar_url_as(size=1024)}")

    @commands.command()
    @commands.guild_only()
    async def icon(self, ctx):
        await ctx.send(f"Icon of {ctx.guild.name}\n{ctx.guild.icon_url_as(size=1024)}")

    @commands.command()
    @commands.guild_only()
    async def whois(self, ctx, user: discord.Member):
        await ctx.message.delete()

        embed = discord.Embed(
            title="{}".format(user.name),
            description="I found this...",
            color=discord.Colour.magenta()
        )

        embed.add_field(name="Name", value="{}#{}".format(
            user.name, user.discriminator), inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Status", value=user.status, inline=True)
        embed.add_field(name="Hightest role", value=user.top_role, inline=True)
        embed.add_field(name="Joined", value=user.joined_at.strftime(
            '%A - %B - %e - %g at %H:%M'), inline=True)
        embed.add_field(name="Nick", value=user.nick, inline=True)
        embed.add_field(name="Created", value=user.created_at.strftime(
            '%A - %B - %e - %g at %H:%M'), inline=True)
        embed.add_field(name="Mention", value=user.mention, inline=True)
        embed.set_thumbnail(url=user.avatar_url)

        try:
            await ctx.send(embed=embed)

        except discord.HTTPException:
            pass

    @commands.command()
    @commands.guild_only()
    async def hackwhois(self, ctx, id: int):

        user = await self.bot.fetch_user(id)
        await ctx.message.delete()

        embed = discord.Embed(
            title="{}".format(user.name),
            description="I found this...",
            color=discord.Colour.magenta()
        )

        embed.add_field(name="Name", value="{}#{}".format(
            user.name, user.discriminator), inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Created", value=user.created_at.strftime(
            '%A - %B - %e - %g at %H:%M'), inline=True)
        embed.set_thumbnail(url=user.avatar_url)

        try:
            await ctx.send(embed=embed)

        except discord.HTTPException:
            pass

    @commands.command()
    @commands.guild_only()
    async def invite(self, ctx):

        toto = await ctx.channel.create_invite(max_uses=15)
        await ctx.send(f"https://discord.gg/{toto.code}")


def setup(bot):
    bot.add_cog(Utilities(bot))
