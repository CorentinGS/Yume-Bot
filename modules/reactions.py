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
    async def arr(self, ctx, message_id: int, role: str, emoji: str):
        # get emoji
        try:
            role = discord.utils.get(ctx.guild.roles, name=role)
        except discord.NotFound:
            return await ctx.send(
                "We can't find the role")
        except discord.InvalidArgument:
            return await ctx.send("We can't find the role.")

        set = await Settings().get_reaction_settings(str(ctx.guild.id))
        await ctx.send(f"{emoji}, {role}")
        set[str(message_id)] = {
            "emoji": emoji.id,
            "role": role.id
        }

        await Settings().set_reaction_settings(str(ctx.guild.id), set)


def setup(bot):
    bot.add_cog(Reactions(bot))
