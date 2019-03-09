import random

import discord
from discord.ext import commands

from modules.utils import lists


class Help(commands.Cog):

    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config


    @commands.command()
    async def commands(self, ctx):
        tip = random.choice(lists.tip)

        await ctx.message.delete()

        embed = discord.Embed(
            set_author='Help',
            color=discord.Colour.magenta()
        )
        embed.set_footer(text=f'Tip: {tip}')

        embed.add_field(
            name="**Commands**", value="[Click here for a full commands list](https://www.yumenetwork.fr)\n", inline=False)
        embed.add_field(
            name="**Invite**", value="[Click Here](https://discordapp.com/oauth2/authorize?client_id=456504213262827524&permissions=8&&scope=bot) to invite the bot", inline=False)
        embed.add_field(
            name="**Support**", value="Join [YumeBot Support](https://invite.gg/yumenetwork) if you want to get help.\n \n"
            "You can also submit your ideas [here](https://github.com/yumenetwork/Yume-Bot/issues/new/choose)", inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
