from discord.ext import commands
import discord.utils

owners = 282233191916634113


def is_owner_check(ctx):
    _id = ctx.message.author.id
    return _id == owners


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
