import re
import sys
import json
import logging
import asyncio

try:
    from discord.ext import commands
    import discord
    print("Discord.py is installed")

except ImportError:
    print("Discord.py is not installed.")
    sys.exit(1)


with open('./config/config.json', 'r') as cjson:
    config = json.load(cjson)

with open('./config/token.json', 'r') as cjson:
    token = json.load(cjson)

PREFIX = config["prefix"]
modules = config["modules"]
OWNER = config["owner_id"]
VERSION = config['version']
TOKEN = token["token"]

bot = commands.Bot(command_prefix=PREFIX)
bot.config = config
bot.ready = False

log = logging.getLogger('bot')
logging.basicConfig(level=logging.WARNING, filename="error.log", filemode="a+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")

print('Connecting...')

bot.remove_command('help')


async def status_task():
    while True:
        names = ['{}help'.format(PREFIX), 'Peace and Dream', 'By Yume']
        for name in names:
            await bot.change_presence(activity=discord.Game(name=name))
            await asyncio.sleep(10)


@bot.event
async def on_connect():
    print("Connected")


@bot.event
async def on_command_error(ctx, exception):
    log.error(str(exception))
    if re.match(r'^The check functions for command.*', str(exception)) is None:
        await ctx.send(str(exception))


@bot.event
async def on_error(event, *args, **kwargs):
    log.error(event + ' : ' + str(args) + " " + str(kwargs))


@bot.event
async def on_ready():
    if not bot.ready:
        bot.ready = True
        loaded = len(modules)
        for module in modules:
            try:
                bot.load_extension('modules.' + module)
            except Exception as e:
                loaded -= 1
                print('Failed to load module {} : {}'.format(module, e))
                log.error('Failed to load module {} : {}'.format(module, e))

        print('Logged in.')
        print('Username : ' + bot.user.name)
        print('ID : ' + str(bot.user.id))
        print('Discord.py version : ' + str(discord.__version__))
        print("Yume bot version : " + VERSION)
        print('Command prefix : ' + PREFIX)
        print('{}/{} modules loaded'.format(loaded, len(modules)))
        print('Press CTRL+C to exit...')
        bot.loop.create_task(status_task())

bot.run(TOKEN)
