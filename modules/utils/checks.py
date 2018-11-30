from discord.ext import commands
import json


with open('config/config.json', 'r') as cjson:
    config = json.load(cjson)

owner = int(config["owner_id"])
DEV = config['dev']


def is_owner_check(ctx):
    _id = ctx.message.author.id
    return _id == owner


def is_owner():
    return commands.check(is_owner_check)


def is_dm_check(ctx):
    if ctx.guild is None:
        return True


def is_dm():
    return commands.check(is_dm_check)


def guild_only():
    async def guild_only_check(ctx):
        if ctx.guild is None:
            return
        return True
    return commands.check(guild_only_check)


# TODO: Rewrite all check and add dev is_check
