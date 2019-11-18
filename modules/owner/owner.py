import json
import random
import secrets
import sys

import discord
from discord.ext import commands

from modules.utils import checks, lists
from modules.utils.db import Settings
from modules.utils.guildy import Setup

with open('./config/config.json', 'r') as cjson:
    config = json.load(cjson)


class Owner(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.command(hidden=True)
    @checks.is_owner()
    async def load(self, ctx, *, cog: str):
        try:
            self.bot.load_extension('modules.' + cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(hidden=True)
    @checks.is_owner()
    async def unload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension('modules.' + cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(hidden=True)
    @checks.is_owner()
    async def reload(self, ctx, *, cog: str):
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

    @commands.command(hidden=True)
    @checks.is_owner()
    async def dm(self, ctx, user: discord.Member, *, content):

        await ctx.message.delete()

        try:
            await ctx.send("{} has been dm".format(user.display_name))
            await user.send(content, delete_after=10)

        except discord.HTTPException:
            pass

    @commands.command(hidden=True)
    @checks.is_owner()
    async def send(self, ctx, channel: discord.TextChannel, *, content):

        await ctx.message.delete()

        try:
            await channel.send(content)

        except discord.HTTPException:
            pass

    @commands.command(hidden=True)
    @checks.is_owner()
    async def speak(self, ctx):

        await ctx.message.delete()

        answer = random.choice(lists.speak)

        await ctx.send(f'{answer}')

    @commands.command(hidden=True)
    @checks.is_owner()
    async def logout(self, ctx):
        await ctx.send('`YumeBot is Logging out...`')
        await self.bot.logout()

    @commands.command(hidden=True)
    @checks.is_owner()
    async def stop(self, ctx):
        await ctx.send("```YumeBot is Stopping...```")
        await self.bot.logout()
        sys.exit(1)

    @commands.command(hidden=True)
    @checks.is_owner()
    async def exit(self):
        sys.exit(1)

    @commands.command(hidden=True)
    @checks.is_owner()
    async def key(self, ctx, name):
        key = secrets.token_urlsafe(20)
        set = await Settings().get_key_settings(str(name))
        set['key'] = key
        await ctx.author.send('The key is : **{}**'.format(str(key)))

    @commands.command(hidden=True)
    @checks.is_owner()
    async def guild(self, ctx):
        await ctx.message.delete()
        em = discord.Embed(timestamp=ctx.message.created_at)
        for guild in self.bot.guilds:
            chan = guild.text_channels[-1]
            try:
                invite = await chan.create_invite()
            except discord.Forbidden:
                em.add_field(
                    name=guild.name, value=f"ID : {guild.id} \nMembers : {len(guild.members)}"
                                           f"\nOwner: {guild.owner} `{guild.owner.id}`", inline=False)
            else:
                em.add_field(
                    name=guild.name, value=f"ID : {guild.id} \nMembers : {len(guild.members)}"
                                           f"\nOwner: {guild.owner} `{guild.owner.id}`\nInvite : {invite.code}",
                    inline=False)

        await ctx.author.send(embed=em)

    @commands.command(hidden=True)
    @checks.is_owner()
    async def check_setup(self, ctx):
        for guild in self.bot.guilds:
            if guild.id == '264445053596991498':
                return
            set = await Settings().get_server_settings(str(guild.id))
            if set["Setup"] is False:
                await Setup.new_guild(guild.id)
                await guild.owner.send(f"Hey ! the YumeBot has received many improvements recently. "
                                       f"We have noticed that your discord: {guild.name} is not configured "
                                       f"for the new version which can lead to errors... "
                                       f"Please execute in a lounge of your discord {guild.name} "
                                       f"the following command: --setting reset")

    @commands.command(hidden=True)
    @checks.is_owner()
    async def check_up(self, ctx):
        for guild in self.bot.guilds:
            set = await Settings().get_server_settings(str(guild.id))
            if set["Setup"] is False:
                await Setup.new_guild(guild.id)
            else:
                await Setup.refresh(guild.id)


    @commands.group(hidden=True)
    @checks.is_owner()
    async def vip(self, ctx):
        if ctx.invoked_subcommand is None:
            return await ctx.send('specify an argument')

    @vip.command(hidden=True)
    async def add(self, ctx, id: int):
        await ctx.message.delete()

        setting = await Settings().get_glob_settings()
        if 'VIP' not in setting:
            setting['VIP'] = []

        if id in setting['VIP']:
            return await ctx.send("This user / guild is already VIP")
        setting['VIP'].append(id)
        await Settings().set_glob_settings(setting)
        await ctx.send(f"{id} is now VIP")

    @vip.command(hidden=True)
    async def remove(self, ctx, id: int):
        await ctx.message.delete()
        setting = await Settings().get_glob_settings()

        if id in setting['VIP']:
            setting['VIP'].remove(id)
            await Settings().set_glob_settings(setting)
            await ctx.send(f"{id} has been remove from VIP")
        else:
            return await ctx.send('User is not VIP')

    @commands.command()
    @checks.is_owner()
    async def botfarms(self, ctx):
        for guild in self.bot.guilds:
            bots = []
            for user in guild.members:
                if user.bot:
                    bots.append(user)
            if len(bots) * 100 / len(guild.members) >= 80:
                await guild.leave()

        await ctx.send("Guild purge is done !")

    @commands.command()
    @checks.is_owner()
    async def activity(self, ctx, *, content):
        await ctx.message.delete()
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(f"{content}"))
        await ctx.author.send(f"New presence : {content}")


    @commands.command()
    @checks.is_owner()
    async def penguin(self, ctx):
        await ctx.message.delete()
        owner_ = int(config["owner_id"])
        owner = ctx.guild.get_member(owner_)

        try:
            role = await ctx.guild.create_role(name="Manchot <3", colour=discord.Colour.blurple())
        except discord.HTTPException:
            return

        try:
            await owner.add_roles(role)
        except discord.HTTPException:
            return



def setup(bot):
    bot.add_cog(Owner(bot))
