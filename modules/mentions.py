import discord
from discord.ext import commands
import json


class Mentions:

    conf = {}

    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

        global conf
        conf = config

    @commands.command(pass_context=True)
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    #@commands.cooldown(1, 20, commands.BucketType.user)
    async def mention(self, ctx, role: str):
        msg = ctx.message
        rolemention = discord.utils.get(ctx.guild.roles, name=role)
        await msg.delete()

        if rolemention.mentionable == False:
            await rolemention.edit(mentionable=True)

        else:
            await ctx.send(rolemention.mention)
            return

        await ctx.send(rolemention.mention)
        await rolemention.edit(mentionable=False)
        return

    @commands.command(pass_context=True)
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    #@commands.cooldown(1, 20, commands.BucketType.user)
    async def annonce(self, ctx, role: str, *, content):
        msg = ctx.message
        rolemention = discord.utils.get(ctx.guild.roles, name=role)
        await msg.delete()

        if rolemention.mentionable == False:
            await rolemention.edit(mentionable=True)

        if rolemention.mentionable == True:
            await ctx.send("{} \n{}".format(rolemention.mention, content))
            return

        await ctx.send("{} \n{}".format(rolemention.mention, content))
        await rolemention.edit(mentionable=False)
        return


def setup(bot):
    bot.add_cog(Mentions(bot, bot.config))
