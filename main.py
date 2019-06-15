import asyncio
import datetime
import json
import logging
import traceback

import discord
from discord.ext import commands

with open('./config/config.json', 'r') as cjson:
    config = json.load(cjson)

with open('./config/token.json', 'r') as cjson:
    token = json.load(cjson)

modules = config["modules"]


def get_prefix(bot, message):
    prefixes = ['--', "y!"]

    if not message.guild:
        return '?'

    return commands.when_mentioned_or(*prefixes)(bot, message)


description = "Yume Bot ! Peace & Dream <3"

log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)


class YumeBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=get_prefix, description=description,
                         pm_help=None, help_attrs=dict(hidden=True), fetch_offline_members=False)

        self.token = token['token']
        self.ready = False
        self.config = config
        self.log = log
        self.owner = config["owner_id"]
        self.guild = config['support']
        self.debug = config['debug']

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.ArgumentParsingError):
            await ctx.send(error)
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send('This is not a command')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("you don't have the permissions to use that command.")
        # raise error

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            print('Logged in.')
            loaded = len(modules)
            for module in modules:
                try:
                    self.load_extension('modules.' + module)
                except Exception as e:
                    loaded -= 1
                    print('Failed to load module {} : {}'.format(module, e))
                    traceback.print_exc()
            print('{}/{} modules loaded'.format(loaded, len(modules)))
        while True:
            names = ['--help', 'Peace and Dream', 'By YumeNetwork']
            for name in names:
                await self.change_presence(activity=discord.Game(name=name))
                await asyncio.sleep(10)

    async def on_resumed(self):
        print('resumed...')

    async def close(self):
        await super().close()
        await self.session.close()

    async def on_guild_join(self, guild):
        await self.wait_until_ready()
        embed = discord.Embed()
        embed.title = 'New Guild'
        embed.set_author(name='{0} <{0.id}>'.format(
            guild.owner), icon_url=guild.owner.avatar_url)
        embed.add_field(name='Server', value='{0.name} <{0.id}>'.format(guild))
        embed.add_field(
            name='Members', value='**{0}**'.format(len(guild.members)))
        embed.color = discord.Color.green()
        embed.timestamp = datetime.datetime.now()
        server = self.get_guild(int(self.guild))
        for chan in server.channels:
            if chan.id == int(self.debug):
                channel = chan
        await channel.send(embed=embed)

    async def on_guild_remove(self, guild):
        await self.wait_until_ready()
        embed = discord.Embed()
        embed.title = 'Left Guild'
        embed.set_author(name='{0} <{0.id}>'.format(
            guild.owner), icon_url=guild.owner.avatar_url)
        embed.add_field(name='Server', value='{0.name} <{0.id}>'.format(guild))
        embed.add_field(
            name='Members', value='**{0}**'.format(len(guild.members)))
        embed.color = discord.Color.red()
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
