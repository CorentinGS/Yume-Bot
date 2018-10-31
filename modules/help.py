import discord
from discord.ext import commands
import json


class Help:

    conf = {}

    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

        global conf
        conf = config

    @commands.command(pass_context=True)
    #@commands.cooldown(1, 60, commands.BucketType.user)
    async def help(self, ctx):

        msg = ctx.message

        await msg.delete()

        embed = discord.Embed(
            set_author='Help',
            color=discord.Colour.magenta()
        )

        embed.add_field(
            name="**Commands**", value="[Click here for a full commands list](https://yumenetwork.gitbook.io/yumebot/)\n", inline=False)
        embed.add_field(
            name="**Invite**", value="[Click Here](https://discordapp.com/api/oauth2/authorize?client_id=456504213262827524&permissions=8&redirect_uri=https%3A%2F%2Fgithub.com%2Fyumenetwork%2FYume-Bot&scope=bot) to invite the bot", inline=False)
        embed.add_field(
            name="**Support**", value="Join [YumeBot Support](https://invite.gg/yumenetwork) if you want to get help.\n \n"
            "You can also submit your ideas [here](https://github.com/yumenetwork/Yume-Bot/issues/new/choose)", inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot, bot.config))
