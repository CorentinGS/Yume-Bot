import discord
from discord.ext import commands
import json


class Whois:

    conf = {}

    def __init__(self, client, config):
        self.client = client
        self.config = config

        global conf
        conf = config

    @commands.command(pass_context=True)
    @commands.guild_only()
    @commands.cooldown(2, 20, commands.BucketType.user)
    async def whois(self, ctx, user: discord.Member):

        msg = ctx.message

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
            await msg.delete()
            return await ctx.send(embed=embed)

        except:
            pass

    @commands.command(pass_context=True)
    @commands.guild_only()
    @commands.cooldown(2, 20, commands.BucketType.user)
    async def hackwhois(self, ctx, id: int):

        user = await self.client.get_user_info(id)
        msg = ctx.message

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
            await msg.delete()
            return await ctx.send(embed=embed)

        except:
            pass


def setup(client):
    client.add_cog(Whois(client, client.config))
