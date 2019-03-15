import random
import secrets
import sys

import discord
from discord.ext import commands

from modules.utils import checks, lists
from modules.utils.db import Settings


class Owner(commands.Cog):

    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.command(hidden=True)
    @checks.is_owner()
    async def load(self, ctx, *, cog:str):
        try:
            self.bot.load_extension('modules.' + cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')    

    @commands.command(hidden=True)
    @checks.is_owner()
    async def unload(self, ctx, *, cog:str):
        try:
            self.bot.unload_extension('modules.' + cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')   

    @commands.command(hidden=True)
    @checks.is_owner()
    async def reload(self, ctx, *, cog:str):
        try:
            self.bot.unload_extension('modules.' + cog)
            self.bot.load_extension('modules.' + cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')   

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
    async def key(self, ctx, name):
        key = secrets.token_urlsafe(20)
        set = await Settings().get_key_settings(str(name))
        set['key'] = key
        set = await Settings().set_key_settings(str(name), set)
        await ctx.author.send('The key is : **{}**'.format(str(key)))

    @commands.command()
    @checks.is_owner()
    async def guild(self, ctx):
        await ctx.message.delete()
        em = discord.Embed(timestamp=ctx.message.created_at)
        for guild in self.bot.guilds:
            em.add_field(
                name=guild.name, value=f"ID : {guild.id} \nMembers : {len(guild.members)}\nOwner: {guild.owner} `{guild.owner.id}`", inline=False)

        await ctx.author.send(embed=em)

    @commands.group()
    @checks.is_owner()
    async def vip(self, ctx):
        if ctx.invoked_subcommand is None:
            return await ctx.send('specify an argument')

    @vip.command()
    async def add(self, ctx, id: int):
        user = await self.bot.get_user_info(id)
        await ctx.message.delete()

        setting = await Settings().get_glob_settings()
        if 'VIP' not in setting:
            setting['VIP'] = []

        if user.id in setting['VIP']:
            return await ctx.send("This user is already VIP")
        setting['VIP'].append(user.id)
        await Settings().set_glob_settings(setting)
        await ctx.send(f"{user} is now VIP")

    @vip.command()
    async def remove(self, ctx, id: int):
        user = await self.bot.get_user_info(id)
        await ctx.message.delete()
        setting = await Settings().get_glob_settings()

        if user.id in setting['VIP']:
            setting['VIP'].remove(user.id)
            await Settings().set_glob_settings(setting)
            await ctx.send(f"{user} has been remove from VIP")

        else:
            return await ctx.send('User is not VIP')

def setup(bot):
    bot.add_cog(Owner(bot))
