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


    @commands.command()
    @checks.is_owner()
    async def guild(self, ctx):
        await ctx.message.delete()
        em = discord.Embed(timestamp=ctx.message.created_at)
        for guild in self.bot.guilds:
            channel = discord.utils.get(guild.text_channels, position=0)
            try:
                toto = await channel.create_invite(max_uses=15)
            except discord.HTTPException:
                em.add_field(name = guild.name, value=f"ID : {guild.id} \nMembers : {len(guild.members)}", inline = False)
            else:
                em.add_field(name = guild.name, value=f"ID : {guild.id} \nMembers : {len(guild.members)} \nInvite : https://discord.gg/{toto.code}", inline = False)
        await ctx.author.send(embed = em)


def setup(bot):
    bot.add_cog(Owner(bot, bot.config))
