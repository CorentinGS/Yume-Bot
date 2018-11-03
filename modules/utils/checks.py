from discord.ext import commands
import json



with open('config/config.json', 'r') as cjson:
    config = json.load(cjson)

owner = config["owner_id"]
DEV = config['dev']

def is_owner():
    async def is_owner_check(ctx):
        _id = ctx.message.author.id
        return _id == owner

    return commands.check(is_owner_check)


def is_dm():
    async def is_dm_check(ctx):
        if ctx.guild is None:
            return True
    return commands.check(is_dm_check)

def is_dev():
    async def is_dev_check(ctx):
        _id = ctx.message.author.id
        for users in DEV:
            return _id == users
    return commands.check(is_dev_check)


def guild_only():
    async def guild_only_check(ctx):
        if ctx.guild is None:
            return
        return True
    return commands.check(guild_only_check)
