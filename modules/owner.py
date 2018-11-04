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

        msg = ctx.message

        try:
            await msg.delete()
            return await ctx.send(content)

        except discord.HTTPException:
            pass

    @commands.command()
    @checks.is_owner()
    async def dm(self, ctx, user: discord.Member, *, content):

        msg = ctx.message

        try:
            await msg.delete()
            await ctx.send("{} has been dm".format(user.display_name))
            return await user.send(content, delete_after=10)

        except discord.HTTPException:
            pass

    @commands.command()
    @checks.is_owner()
    async def send(self, ctx, channel: discord.TextChannel, *, content):

        msg = ctx.message

        try:
            await msg.delete()
            return await channel.send(content)

        except discord.HTTPException:
            pass

    @commands.command()
    @checks.is_owner()
    async def speak(self, ctx):

        msg = ctx.message
        await msg.delete()

        answer = random.choice(lists.speak)

        return await ctx.send(f'{answer}')

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

        # TODO: Commands group for debugging...

def setup(bot):
    bot.add_cog(Owner(bot, bot.config))
