import json

from discord.ext import commands

from modules.utils.db import Settings

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


async def is_mod_check(ctx):
    set = await Settings().get_server_settings(str(ctx.guild.id))
    auth = ctx.message.author
    if auth == ctx.message.guild.owner:
        return True 
    if ctx.guild is None:
        return
    for role in auth.roles:
        if str(role.id) in set['Mods']:
            return True


def is_mod():
    return commands.check(is_mod_check)


async def is_admin_check(ctx):
    set = await Settings().get_server_settings(str(ctx.guild.id))
    auth = ctx.message.author
    if auth == ctx.message.guild.owner:
        return True 
    if ctx.guild is None:
        return False
    for role in auth.roles:
        if str(role.id) in set['Admins']:
            return True


def is_admin():
    return commands.check(is_admin_check)

# TODO: Rewrite all check and add dev is_check
