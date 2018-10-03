import discord
from discord.ext import commands
import json


class Help:

    conf = {}

    def __init__(self, client, config):
        self.client = client
        self.config = config

        global conf
        conf = config

    @commands.command(pass_context=True)
    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def help(self, ctx):

        msg = ctx.message
        embed = discord.Embed(
            set_author="Help Menu",
            color=discord.Colour.orange()
        )

        embed.add_field(
            name="Help", value="Display this message", inline=False)

        embed.add_field(name="Whois", value="Display whois of someone", inline=False)
        embed.add_field(name="HackWhois", value="Display hackwhois of someone", inline=False)
        embed.add_field(name="Credit", value="Display the credit message", inline=False)
        embed.add_field(name="Info", value="Display informations about the server", inline=False)
        embed.add_field(name="Ping", value="Pong !!!", inline=False)
        embed.add_field(name='Rd', value='Convert the date into Republican Date', inline=False)
        embed.add_field(name='Ddg', value='Search on the web with DuckDuckGo', inline=False)
        embed.add_field(name='Qwant', value='Search on the web with Qwant', inline=False)
        embed.add_field(name='Discordpy', value='Search on the discord py doc', inline=False)
        embed.add_field(name="Ban", value="Ban an user", inline=False)
        embed.add_field(name="HackBan", value="HackBan an user", inline=False)
        embed.add_field(name="Kick", value="Kick an user", inline=False)
        embed.add_field(name="Mute", value="Mute an user", inline=False)
        embed.add_field(name='Unmute', value='Unmute an user', inline=False)
        embed.add_field(name='Purge', value='Purge the current channel', inline=False)
        embed.add_field(name="Mention", value="Mention a role", inline=False)
        embed.add_field(name="Annonce", value="Fait une annonce", inline=False)

        try:
            await msg.delete()
            return await ctx.send(embed=embed)

        except:
            pass


def setup(client):
    client.add_cog(Help(client, client.config))
