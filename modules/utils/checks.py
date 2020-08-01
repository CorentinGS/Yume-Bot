#  Copyright (c) 2019.
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


import json

from discord.ext import commands

from modules.sql.guilddb import GuildDB
from modules.sql.userdb import UserDB

with open('config/config.json', 'r') as cjson:
    config = json.load(cjson)

owner = int(config["owner_id"])
DEV = config['dev']
princes = [292362017006944256, 511135694207451146, 282233191916634113, 252393780173471745]


def is_owner_check(ctx):
    return ctx.message.author.id == owner


def is_owner():
    return commands.check(is_owner_check)


def is_prince_check(ctx):
    return ctx.message.author.id in princes


def is_prince():
    return commands.check(is_prince_check)


async def is_mod_check(ctx):
    guild = GuildDB.get_one(ctx.guild.id)
    mods = GuildDB.get_mod_roles(guild)
    admins = GuildDB.get_admin_roles(guild)

    auth = ctx.message.author
    if ctx.guild is None:
        return
    if auth == ctx.guild.owner:
        return True
    for role in auth.roles:
        if role.id in mods or role.id in admins:
            return True


def is_mod():
    return commands.check(is_mod_check)


async def is_admin_check(ctx):
    guild = GuildDB.get_one(ctx.guild.id)
    admins = GuildDB.get_admin_roles(guild)

    auth = ctx.message.author
    if ctx.guild is None:
        return False
    if auth == ctx.message.guild.owner:
        return True
    for role in auth.roles:
        if role.id in admins:
            return True


def is_admin():
    return commands.check(is_admin_check)


async def is_immune(message):
    guild = GuildDB.get_one(message.guild.id)
    admins = GuildDB.get_admin_roles(guild)
    auth = message.author
    if message.guild is None:
        return False
    if auth == message.guild.owner:
        return True
    for role in auth.roles:
        if role.id in admins:
            return True


async def is_vip_check(ctx):
    vips = UserDB.get_vips()
    if ctx.message.author.id in vips:
        return True
    else:
        return False


def is_vip():
    return commands.check(is_vip_check)
