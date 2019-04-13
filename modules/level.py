import random
from random import randint

import discord
from discord.ext import commands

from modules.utils import checks, lists
from modules.utils.db import Settings


class Level(commands.Cog):

    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.command()
    async def rank(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.message.author

        set = await Settings().get_user_settings(str(ctx.message.guild.id))

        if str(user.id) not in set:

            d = {"level": 0, "xp": 0, "reach": 20}
            set[str(user.id)] = d
            await Settings().set_user_settings(str(ctx.message.guild.id), set)

        dic = set[str(user.id)]
        em = discord.Embed()
        em.set_author(name=user.name, icon_url=user.avatar_url)
        em.add_field(name="**Level**", value=dic["level"])
        em.add_field(name="**Progress**",
                     value="{} / {}".format(dic['xp'], dic['reach']))
        await ctx.send(embed=em)

    @commands.group()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def level(self, ctx):
        if ctx.invoked_subcommand is None:
            # await ctx.invoke(self.get)
            return

    @level.command()
    @commands.has_permissions(administrator=True)
    async def config(self, ctx, level: int, role: str):
        set = await Settings().get_server_settings(str(ctx.message.guild.id))
        if not "levels" in set:
            set["levels"] = {}
        await Settings().set_server_settings(str(ctx.message.guild.id), set)
        try:
            rolemention = discord.utils.get(ctx.guild.roles, name=role)
        except discord.NotFound:
            return await ctx.send("We can't find the role. Be sure to follow the syntax as in the exemple : **--level set 3 test_role")


        toto = set["levels"]
        toto[str(level)] = str(rolemention.id)

        await Settings().set_server_settings(str(ctx.message.guild.id), set)

    @commands.Cog.listener()
    async def on_message(self, message):
        user = message.author

        set = await Settings().get_user_settings(str(message.guild.id))
        toto = await Settings().get_server_settings(str(message.guild.id))

        if not str(user.id) in set:
            d = {"level": 0, "xp": 0, "reach": 20}
            set[str(user.id)] = d
            print(set[str(user.id)])

        if not "levels" in toto:
            toto["levels"] = {}


        await Settings().set_server_settings(str(message.guild.id), toto)
        await Settings().set_user_settings(str(message.guild.id), set)


        dic = set[str(user.id)]
        gain = randint(2, 7)

        dic['xp'] += gain

        if dic['xp'] >= dic['reach']:
            dic['reach'] = dic['reach'] * 2
            dic['xp'] = 0
            dic['level'] += 1

            lvl = toto["levels"]
            for key in lvl:
                if int(key) == dic['level']:
                    role = discord.utils.get(
                        message.guild.roles, id=int(lvl[key]))
                    await user.add_roles(role)

            await message.channel.send("{} is now level {}.".format(user.name, dic['level']), delete_after=3)

        set[str(user.id)] = dic
        await Settings().set_user_settings(str(message.guild.id), set)


def setup(bot):
    bot.add_cog(Level(bot))
