import datetime
import json
import logging
import sys
import traceback

import discord
from discord.ext import commands

with open('./config/config.json', 'r') as cjson:
    config = json.load(cjson)

with open('./config/token.json', 'r') as cjson:
    token = json.load(cjson)

modules = config["modules"]


def get_prefix(bot, message):
    prefixes = ['--', "y!", "yume", "yum"]

    if not message.guild:
        return '?'

    return commands.when_mentioned_or(*prefixes)(bot, message)


description = "Yume Bot ! Peace & Dream <3"

'''
log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)
'''

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class YumeBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=get_prefix, description=description, activity=discord.Game(name="Commands: --help"),
                         pm_help=None, help_attrs=dict(hidden=True), fetch_offline_members=False)

        self.uptime = datetime.datetime.utcnow()
        self.token = token['token']
        self.ready = False
        self.config = config
        self.owner = config["owner_id"]
        self.guild = config['support']
        self.debug = config['debug']
        self.remove_command("help")

        # self.session = aiohttp.ClientSession(loop=self.loop)

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

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send('This command cannot be used in private messages.')
        elif isinstance(error, commands.DisabledCommand):
            await ctx.author.send('Sorry. This command is disabled and cannot be used.')
        if isinstance(error, commands.BotMissingPermissions):
            return await ctx.send("I don't have the required permissions to perform this command. Please give me administrator permissions")
        elif isinstance(error, commands.CommandInvokeError):
            original = error.original
            if not isinstance(original, discord.HTTPException):
                print(f'In {ctx.command.qualified_name}:', file=sys.stderr)
                traceback.print_tb(original.__traceback__)
                print(f'{original.__class__.__name__}: {original}', file=sys.stderr)
        elif isinstance(error, commands.ArgumentParsingError):
            await ctx.send(error)

    async def close(self):
        await super().close()

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
