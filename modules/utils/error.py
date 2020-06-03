import discord


class Errors:

    @staticmethod
    async def forbidden_error():
        em = discord.Embed(color=discord.Colour.red())
        msg: str = f" ❌ I'm not allowed to do that !"
        em.description = msg
        return em

    @staticmethod
    async def check_error(ctx):
        em = discord.Embed(color=discord.Colour.red())
        msg: str = f" ⛔ **{ctx.author.display_name}**, you can't do that !"
        em.description = msg
        return em
