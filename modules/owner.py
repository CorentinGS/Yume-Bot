import sys
import random
import discord

from discord.ext import commands
from modules.utils import checks
from modules.utils import lists


class Owner:

    conf = {}

    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

        global conf
        conf = config

    @commands.command(aliases=['say'])
    @checks.is_owner()
    async def echo(self, ctx, *, content):

        await ctx.message.delete()

        try:
            await ctx.send(content)

        except discord.HTTPException:
            pass

    @commands.command()
    @checks.is_owner()
    async def dm(self, ctx, user: discord.Member, *, content):

        await ctx.message.delete()

        try:
            await ctx.send("{} has been dm".format(user.display_name))
            await user.send(content, delete_after=10)

        except discord.HTTPException:
            pass

    @commands.command()
    @checks.is_owner()
    async def send(self, ctx, channel: discord.TextChannel, *, content):

        await ctx.message.delete()

        try:
            await channel.send(content)

        except discord.HTTPException:
            pass

    @commands.command()
    @checks.is_owner()
    async def speak(self, ctx):

        await ctx.message.delete()

        answer = random.choice(lists.speak)

        await ctx.send(f'{answer}')

    @commands.command()
    @checks.is_owner()
    async def logout(self, ctx):
        await ctx.send('`YumeBot is Logging out...`')
        await self.bot.logout()

    @commands.command()
    @checks.is_owner()
    async def stop(self, ctx):
        await ctx.send("```YumeBot is Stopping...```")
        await self.bot.logout()
        sys.exit(1)

    @commands.command()
    @checks.is_owner()
    async def exit(self, ctx):
        sys.exit(1)

    @commands.command()
    @checks.is_owner()
    async def guild(self, ctx):
        await ctx.message.delete()
        em = discord.Embed(timestamp=ctx.message.created_at)
        for guild in self.bot.guilds:
            em.add_field(
                name=guild.name, value=f"ID : {guild.id} \nMembers : {len(guild.members)}\nOwner: {guild.owner} `{guild.owner.id}`", inline=False)

        await ctx.author.send(embed=em)


def setup(bot):
    bot.add_cog(Owner(bot, bot.config))
