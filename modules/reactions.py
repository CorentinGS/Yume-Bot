import typing

import discord
from discord.ext import commands

from modules.utils.db import Settings


class Reactions(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.command()
    @commands.guild_only()
    async def arr(self, ctx, message_id: int, role: typing.Union[str, discord.Role],
                  emoji: typing.Union[str, discord.Emoji]):

        if not role is discord.Role:
            try:
                role = discord.utils.get(ctx.guild.roles, name=role)
            except discord.NotFound:
                return await ctx.send(
                    "We can't find the role")
            except discord.InvalidArgument:
                return await ctx.send("We can't find the role.")

        set = await Settings().get_reaction_settings(str(ctx.guild.id))
        x = await ctx.send(f"{emoji}, {role}")
        try:
            await x.add_reaction(emoji)
        except discord.InvalidArgument:
            return await ctx.send("The emoji isn't valid.")
        except discord.NotFound:
            return await ctx.send("The emoji isn't valid.")

        if emoji is discord.Emoji:
            emoji = emoji.id

        msg = set[str(message_id)]
        msg[str(emoji)] = str(role.id)

        await Settings().set_reaction_settings(str(ctx.guild.id), set)


def setup(bot):
    bot.add_cog(Reactions(bot))
