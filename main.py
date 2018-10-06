import asyncio
import json
import datetime
import logging
import re
import os
import sys
import datetime
from itertools import cycle
import pymongo
from pymongo import MongoClient


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


desc = " "
PREFIX = config["prefix"]
modules = config["modules"]
OWNER = config["owner_id"]
TOKEN = token["token"]

global bot
bot = commands.Bot(command_prefix=PREFIX, description=desc)
bot.config = config

bot.remove_command('help')


async def status_task():
    while True:
        await bot.change_presence(activity=discord.Game(name=PREFIX + "help"))
        await asyncio.sleep(10)
        # await bot.change_presence(activity=discord.Game(name=desc))
        await bot.change_presence(activity=discord.Game(name="Peace and Dream"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Game(name="By Yume"))
        await asyncio.sleep(10)

@bot.event
async def on_connect():
    print("Connected")


@bot.event
async def on_command_error(ctx, exception):
    logging.basicConfig(level=logging.WARNING, filename="error.log", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    logging.error(str(exception))
    if re.match(r'^The check functions for command.*', str(exception)) is None:
        await ctx.send(str(exception))


@bot.event
async def on_error(event, *args, **kwargs):
    logging.basicConfig(level=logging.WARNING, filename="error.log", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    logging.error(event + " -> " + str(args) + " " + str(kwargs))


@bot.event
async def on_ready():
    print('Logged in.')
    print('Username -> ' + bot.user.name)
    print('ID -> ' + str(bot.user.id))
    print("Discord.py version info : " + str(discord.__version__))
    print('Command prefix -> ' + PREFIX)
    print("Press CTRL+C --> exit...")
    bot.loop.create_task(status_task())


def ready(bot, config):
    for module in modules:
        try:
            print('Try bot.load_extension = ' + module)
            bot.load_extension("modules." + module)
            print('bot.load_extension is working')
        except Exception as e:
            raise Exception(e)


ready(bot, config)

bot.run(TOKEN)
