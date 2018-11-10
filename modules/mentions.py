import discord
from discord.ext import commands


class Mentions:

    conf = {}

    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

        global conf
        conf = config

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    #  @commands.cooldown(1, 20, commands.BucketType.user)
    async def mention(self, ctx, role: str):

        await ctx.message.delete()
        rolemention = discord.utils.get(ctx.guild.roles, name=role)

        if not rolemention.mentionable:
            await rolemention.edit(mentionable=True)

        await ctx.send(rolemention.mention)
        await rolemention.edit(mentionable=False)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    #  @commands.cooldown(1, 20, commands.BucketType.user)
    async def annonce(self, ctx, role: str, *, content):
        await ctx.message.delete()
        rolemention = discord.utils.get(ctx.guild.roles, name=role)

        if not rolemention.mentionable:
            await rolemention.edit(mentionable=True)

        await ctx.send("{} \n{}".format(rolemention.mention, content))
        await rolemention.edit(mentionable=False)


def setup(bot):
    bot.add_cog(Mentions(bot, bot.config))
