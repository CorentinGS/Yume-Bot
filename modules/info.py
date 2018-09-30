import discord
from discord.ext import commands
import json

class Info:

    conf = {}

    def __init__(self, client, config):
        self.client = client
        self.config = config

        global conf
        conf = config


    @commands.command(pass_context = True)
    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def info(self, ctx):
        msg = ctx.message
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

        embed.add_field(name="Name", value=server.name, inline=True)
        embed.add_field(name="ID", value=server.id, inline=True)
        embed.add_field(name="Roles", value=len(server.roles), inline=True)
        embed.add_field(name="Members", value=len(server.members), inline=True)
        embed.add_field(name="Channels", value=len(server.channels), inline=True)
        embed.add_field(name="Security", value=server.verification_level, inline=True)
        embed.add_field(name="Region", value=server.region, inline=True)
        embed.add_field(name="Owner", value=server.owner, inline=True)
        embed.add_field(name="2AF", value=af, inline=False)
        embed.add_field(name="created at", value=server.created_at.strftime('%A - %B - %e at %H:%M'), inline=False)
        embed.set_thumbnail(url=server.icon_url)

        try:
            await msg.delete()
            return await ctx.send(embed=embed)

        except:
            pass

    @commands.command(pass_context = True)
    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def members(self, ctx):
        msg = ctx.message
        server = ctx.message.guild

        embed = discord.Embed(
            title="{}".format(ctx.message.guild.name),
            description="I found this...",
            color=discord.Colour.dark_gold()
        )

        embed.add_field(name="Members", value=len(server.members), inline=True)
        embed.set_thumbnail(url=server.icon_url)

        try:
            await msg.delete()
            return await ctx.send(embed=embed)

        except:
            pass


    @commands.command(pass_context = True)
    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def owner(self, ctx):
        msg = ctx.message
        server = ctx.message.guild

        embed = discord.Embed(
            title="{}".format(ctx.message.guild.name),
            description="I found this...",
            color=discord.Colour.dark_gold()
        )

        embed.add_field(name="Members", value=len(server.owner.mention), inline=True)
        embed.set_thumbnail(url=server.icon_url)

        try:
            await msg.delete()
            return await ctx.send(embed=embed)

        except:
            pass



def setup(client):
    client.add_cog(Info(client, client.config))
