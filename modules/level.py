import collections
from random import randint
import asyncio


import discord
from discord.ext import commands

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
            d = {"level": 0, "xp": 0, "reach": 20, "total": 0}
            set[str(user.id)] = d
            await Settings().set_user_settings(str(ctx.message.guild.id), set)

        dic = set[str(user.id)]
        em = discord.Embed()
        em.set_author(name=user.name, icon_url=user.avatar_url)
        em.add_field(name="**Level**", value=dic["level"])
        em.add_field(name="**Progress**",
                     value="{} / {}".format(dic['xp'], dic['reach']))
        await ctx.send(embed=em)

    @commands.command()
    async def leaderboard(self, ctx):
        set = await Settings().get_user_settings(str(ctx.message.guild.id))
        ranks = {}
        x = 0
        em = discord.Embed(
            description="ScoreBoard",
            color=discord.Colour.magenta()
        )

        for user in set.keys():
            if user == '_id':
                continue
            toto = set[str(user)]
            ranks[user] = toto["total"]

        sorted_x = sorted(ranks.items(), key=lambda kv: kv[1], reverse=True)
        sorted_dict = collections.OrderedDict(sorted_x).copy()
        await asyncio.sleep(15)
        for user in sorted_dict.keys():
            member = discord.utils.get(ctx.guild.members, id=int(user))
            if member is None:
                del sorted_dict[user]
            else:
                x += 1
                level = set[str(user)]['level']
                total = set[str(user)]['total']
                em.add_field(name=f"{x} - {member.name}", value=f"Level : {level} \nTotal xp : {total}", inline=False)

                if x == 10:
                    break

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
            print(rolemention.id)
        except discord.NotFound:
            return await ctx.send(
                "We can't find the role. Be sure to follow the syntax as in the exemple : **--level set 3 test_role**")
        except discord.InvalidArgument:
            return await ctx.send("We can't find the role. Be sure to follow the syntax as in the exemple : **--level set 3 test_role**")

        toto = set["levels"]
        toto[str(level)] = str(rolemention.id)
        set["levels"] = toto

        await Settings().set_server_settings(str(ctx.message.guild.id), set)
        await ctx.send("Level setup")

        # TODO: Améliorer le message de setup
        # TODO: Ajouter la possibilité de mentioner le role.

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """

        :param message: The message that has been sent
        """
        user = message.author

        if user.bot is True or message.guild is None:
            return

        set = await Settings().get_user_settings(str(message.guild.id))
        toto = await Settings().get_server_settings(str(message.guild.id))

        if not str(user.id) in set:
            d = {"level": 0, "xp": 0, "reach": 20, "total": 0}
            set[str(user.id)] = d

        await Settings().set_user_settings(str(message.guild.id), set)

        dic = set[str(user.id)]
        gain = randint(2, 7)

        dic['xp'] += gain
        dic['total'] += dic['xp']

        if dic['xp'] >= dic['reach']:
            dic['reach'] = round(dic['reach'] * 1.5)
            dic['xp'] = 0
            dic['level'] += 1

            lvl = toto["levels"]
            for key in lvl:
                if int(key) == dic['level']:
                    try:
                        role = discord.utils.get(
                            message.guild.roles, id=int(lvl[key]))
                    except discord.NotFound:
                        break
                    else:
                        continue

                    try:
                        await user.add_roles(role)
                    except discord.Forbidden:
                        break
                    except discord.InvalidArgument:
                        break
            try:
                await message.channel.send("{} is now level {}.".format(user.name, dic['level']), delete_after=3)
            except discord.Forbidden:
                pass

                # TODO: Eviter la duplication du msg de lvl up
        set[str(user.id)] = dic
        await Settings().set_user_settings(str(message.guild.id), set)


# TODO: Ajouter des commandes pour voir les roles et un leaderboard


def setup(bot):
    bot.add_cog(Level(bot))
