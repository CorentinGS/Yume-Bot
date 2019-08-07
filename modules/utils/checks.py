import json

from discord.ext import commands

from modules.utils.db import Settings

with open('config/config.json', 'r') as cjson:
    config = json.load(cjson)

owner = int(config["owner_id"])
DEV = config['dev']


def is_owner_check(ctx):
    return ctx.message.author.id == owner


def is_owner():
    return commands.check(is_owner_check)


async def is_mod_check(ctx):
    set = await Settings().get_server_settings(str(ctx.guild.id))
    auth = ctx.message.author
    if ctx.guild is None:
        return
    if auth == ctx.message.guild.owner:
        return True
    for role in auth.roles:
        if str(role.id) in set['Mods']:
            return True


def is_mod():
    return commands.check(is_mod_check)


async def is_admin_check(ctx):
    set = await Settings().get_server_settings(str(ctx.guild.id))
    auth = ctx.message.author
    if ctx.guild is None:
        return False
    if auth == ctx.message.guild.owner:
        return True
    for role in auth.roles:
        if str(role.id) in set['Admins']:
            return True


def is_admin():
    return commands.check(is_admin_check)


async def is_vip_check(ctx):
    glob = await Settings().get_glob_settings()
    if ctx.message.guild.id in glob["VIP"] or ctx.message.author.id in glob["VIP"]:
        return True
    else:
        return False


def is_vip():
    return commands.check(is_vip_check)
