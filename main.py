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

import datetime
import json
import logging
import sys
import traceback

import discord
from discord.ext import commands

from modules.utils.error import Errors

with open("./config/config.json", "r") as cjson:
    config = json.load(cjson)

with open("./config/token.json", "r") as cjson:
    token = json.load(cjson)

modules = config["modules"]


def get_prefix(bot, message):
    prefixes = ["--", "y!", "yume", "yum", "yume ", "yum ", "yume!"]

    if not message.guild:
        return "?"

    return commands.when_mentioned_or(*prefixes)(bot, message)


description = "Yume Bot ! Peace & Dream <3"

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


class YumeBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=get_prefix,
            description=description,
            activity=discord.Game(name="Loading..."),
            pm_help=None,
            help_attrs=dict(hidden=True),
            fetch_offline_members=False,
        )

        self.uptime = datetime.datetime.utcnow()
        self.token = token["token"]
        self.ready = False
        self.config = config
        self.owner = config["owner_id"]
        self.guild = config["support"]
        self.debug = config["debug"]
        self.remove_command("help")

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            print("Logged in.")
            loaded = len(modules)
            for module in modules:
                try:
                    self.load_extension("modules." + module)
                except Exception as e:
                    loaded -= 1
                    print("Failed to load module {} : {}".format(module, e))
                    traceback.print_exc()
            print("{}/{} modules loaded".format(loaded, len(modules)))

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            em = await Errors.check_error(ctx)
            return await ctx.send(embed=em)
        elif isinstance(error, commands.UserInputError):
            command = bot.get_command(f"help {ctx.command.name}")
            await ctx.invoke(command)
            # TODO: Check if there is a group command or something like this
        elif isinstance(error, commands.CommandInvokeError):
            original = error.original
            if not isinstance(original, discord.HTTPException):
                print(f"In {ctx.command.qualified_name}:", file=sys.stderr)
                traceback.print_tb(original.__traceback__)
                print(f"{original.__class__.__name__}: {original}", file=sys.stderr)
            elif isinstance(original, discord.Forbidden):
                try:
                    em = await Errors.forbidden_error()
                    await ctx.send(embed=em)
                except discord.Forbidden:
                    return

    async def close(self):
        await super().close()

    async def on_guild_join(self, guild):
        await self.wait_until_ready()
        embed = discord.Embed(colour=discord.Color.green())
        embed.title = "New Guild"
        embed.set_author(
            name="{0} <{0.id}>".format(guild.owner), icon_url=guild.owner.avatar_url
        )
        embed.add_field(name="Server", value="{0.name} <{0.id}>".format(guild))
        embed.add_field(name="Members", value="**{0}**".format(len(guild.members)))
        embed.timestamp = datetime.datetime.now()
        server = self.get_guild(int(self.guild))
        for chan in server.channels:
            if chan.id == int(self.debug):
                channel = chan
        await channel.send(embed=embed)

    async def on_guild_remove(self, guild):
        await self.wait_until_ready()
        embed = discord.Embed(colour=discord.Color.red())
        embed.title = "Left Guild"
        embed.set_author(
            name="{0} <{0.id}>".format(guild.owner), icon_url=guild.owner.avatar_url
        )
        embed.add_field(name="Server", value="{0.name} <{0.id}>".format(guild))
        embed.add_field(name="Members", value="**{0}**".format(len(guild.members)))
        embed.timestamp = datetime.datetime.now()
        server = self.get_guild(int(self.guild))
        for chan in server.channels:
            if chan.id == int(self.debug):
                channel = chan
        await channel.send(embed=embed)

    def run(self):
        super().run(self.token, reconnect=True)


bot = YumeBot()
bot.run()
