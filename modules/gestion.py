import asyncio
import json
import random

import discord
from discord.ext import commands

from modules.utils import checks, lists
from modules.utils.db import Settings
from modules.utils.format import Embeds

with open('./config/config.json', 'r') as cjson:
    config = json.load(cjson)

CHANGELOG = config['changelog']
SUGGESTION = config['suggestion']
FEEDBACK = config["feedback"]
GUILD = config['support']


class Gestion(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.command()
    @checks.is_owner()
    async def changelog(self, ctx, version: str):
        channel = self.bot.get_channel(int(CHANGELOG))
        tip = random.choice(lists.tip)

        await ctx.send("{}, Tell me your Changelog".format(ctx.message.author.mention), delete_after=500)

        def check(m):
            if m.author == ctx.message.author:
                return True
            else:
                return False

        msg = await self.bot.wait_for('message', timeout=240, check=check)

        await msg.delete()

        em = discord.Embed(timestamp=ctx.message.created_at)
        em.set_author(name=f"ℹ Changelog, {version}")
        em.set_footer(text=f'Tip: {tip}')
        em.description = f'{msg.content}'

        await channel.send(embed=em)

    @commands.command()
    async def suggestion(self, ctx, *, content: str):

        guild = self.bot.get_guild(int(GUILD))
        for chan in guild.channels:
            if chan.id == int(SUGGESTION):
                channel = chan
        tip = random.choice(lists.tip)

        await ctx.message.delete()

        em = discord.Embed(timestamp=ctx.message.created_at)
        em.set_author(
            name=f"Suggestion from {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        em.set_footer(text=f'Tip: {tip}')
        em.description = f'{content}'

        reactions = ['✅', '❌', '➖']

        msg = await channel.send(embed=em)

        for reaction in reactions:
            await msg.add_reaction(reaction)

    @commands.command()
    async def feedback(self, ctx):

        await ctx.message.delete()

        auth = ctx.message.author
        guild = ctx.message.guild

        # owner = await self.bot.get_user_info(OWNER)
        server = self.bot.get_guild(int(GUILD))
        for chan in server.channels:
            if chan.id == int(FEEDBACK):
                channel = chan

        await ctx.send("{}, Tell me your feedback".format(ctx.message.author.mention), delete_after=70)

        def check(m):
            if m.author == ctx.message.author:
                return True
            else:
                return False

        try:
            msg = await self.bot.wait_for('message', timeout=60.0, check=check)

        except asyncio.TimeoutError:
            await ctx.send('👎')
            success = False
            return

        else:
            success = True
            await ctx.send('👍')

        msg.delete()
        em = await Embeds().format_feedback_embed(ctx, auth, guild, success, msg)
        await channel.send(embed=em)


def setup(bot):
    bot.add_cog(Gestion(bot))
