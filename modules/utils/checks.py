from discord.ext import commands
import json

with open('modules/utils/tag.json', 'r') as cjson:
    check = json.load(cjson)


def is_owner():
    async def is_owner_check(ctx):
        _id = ctx.message.author.id
        if owner in check:
            for owners in owner:
                return _id == owners

    return commands.check(is_owner_check)


def is_dm:()
    async def is_dm_check(ctx):
        if ctx.guild is None:
            return True
    return commands.check(is_dm_check)

def is_dev():
    async def is_dev_check(ctx):
        _id = ctx.message.author.id
        if dev in check:
            for users in dev:
                return _id == users
    return commands.check(is_dev_check)


def guild_only():
    async def guild_only_check(ctx):
        if ctx.guild is None:
            return
        return True
    return commands.check(guild_only_check)
