import discord
from discord.ext import commands
from modules.utils import checks
import json
from datetime import datetime
import os
import psutil


class Credit:

    conf = {}

    def __init__(self, client, config):
        self.client = client
        self.config = config
        self.process = psutil.Process(os.getpid())

        global conf
        conf = config

    @commands.command(pass_context=True)
    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def credit(self, ctx):

        with open('./config/config.json', 'r') as cjson:
            config = json.load(cjson)

        VERSION = config["version"]
        OWNER = config["owner_id"]

        message = ctx.message
        await message.delete()
        owner = await self.client.get_user_info(OWNER)

        embed = discord.Embed(
            title="Credit",
            description="I found this...",
            color=discord.Colour.blue()
        )

        embed.add_field(name="Dev", value="{}#{}".format(
            owner.name, owner.discriminator), inline=True)
        embed.add_field(name="ID", value=owner.id, inline=True)
        embed.add_field(name="Lib", value=discord.__version__, inline=True)
        embed.add_field(name="Version", value=VERSION, inline=True)
        embed.set_thumbnail(url=owner.avatar_url)

        return await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def lib(self, ctx):

        message = ctx.message
        await message.delete()

        embed = discord.Embed(
            title="Credit",
            description="I found this...",
            color=discord.Colour.blue()
        )

        embed.add_field(name="Lib", value=discord.__version__, inline=True)
        embed.add_field(
            name="Github", value="https://github.com/Rapptz/discord.py/tree/rewrite", inline=True)
        embed.add_field(name="Documentation",
                        value="https://discordpy.readthedocs.io/en/rewrite/index.html", inline=True)
        embed.add_field(name="Discord Support",
                        value="https://discordapp.com/invite/r3sSKJJ", inline=True)

        return await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def about(self, ctx):

        message = ctx.message
        await message.delete()

        ramUsage = self.process.memory_full_info().rss / 1024**2

        embed = discord.Embed(
            title="About",
            color=ctx.me.top_role.colour
        )

        embed.add_field(name="RAM", value=f"{ramUsage:.2f} MB", inline=True)
        embed.add_field(name="Servers", value=len(
            self.client.guilds), inline=True)

        return await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Credit(client, client.config))
