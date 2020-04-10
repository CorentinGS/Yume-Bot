#  Copyright (c) 2020.
#  MIT License
#
#  Copyright (c) 2019 YumeNetwork
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
import json
import random
import sys

import discord
from discord.ext import commands

from modules.sql.userdb import UserDB
from modules.utils import checks, lists

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
    async def guilds(self, ctx):
        await ctx.message.delete()
        await ctx.send("Searching guilds...")
        invites = []
        i = False
        em = discord.Embed(timestamp=ctx.message.created_at)
        print("Loading guilds")
        for guild in self.bot.guilds:
            # await asyncio.sleep(500)
            if not guild.unavailable:
                try:
                    invites = await guild.invites()
                except discord.HTTPException:
                    pass
                if len(invites) > 0:

                    em.add_field(
                        name=guild.name, value=f"ID : {guild.id} \nMembers : {len(guild.members)}"
                                               f"\nOwner: {guild.owner} `{guild.owner_id}`\nInvite : {invites[0].code}",
                        inline=False)
                else:
                    for chan in guild.text_channels:
                        try:
                            invite = await chan.create_invite()
                        except discord.Forbidden:
                            pass
                        else:
                            em.add_field(
                                name=guild.name, value=f"ID : {guild.id} \nMembers : {len(guild.members)}"
                                                       f"\nOwner: {guild.owner} `{guild.owner_id}`\nInvite : {invite.code}",
                                inline=False)
                            i = True
                            break
                    if not i:
                        em.add_field(
                            name=guild.name, value=f"ID : {guild.id} \nMembers : {len(guild.members)}"
                                                   f"\nOwner: {guild.owner} `{guild.owner_id}`", inline=False)
            print("Sending embed")
            await ctx.author.send(embed=em)

    @commands.group(hidden=True)
    @checks.is_owner()
    async def vip(self, ctx):
        if ctx.invoked_subcommand is None:
            return await ctx.send('specify an argument')

    @vip.command(hidden=True)
    async def add(self, ctx, id: int):
        await ctx.message.delete()
        user = UserDB.get_one(id)
        UserDB.set_vip(user)

        await ctx.send(f"{id} is now VIP")

    @vip.command(hidden=True)
    async def remove(self, ctx, id: int):
        await ctx.message.delete()
        user = UserDB.get_one(id)
        UserDB.unset_vip(user)
        await ctx.send(f"{id} has been remove from VIP")

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
