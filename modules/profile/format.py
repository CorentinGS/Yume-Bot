import discord


class Embeds:

    @staticmethod
    async def get_lover(user: discord.Member, lover: discord.User) -> discord.Embed:
        em = discord.Embed(color=discord.Colour.blue())
        msg: str = f"♥️️{user.name}#{user.discriminator} is married with {lover.name}#{lover.discriminator}"
        em.description = msg
        return em

    @staticmethod
    async def ask_to_marry(user: discord.Member, lover: discord.Member) -> discord.Embed:
        em = discord.Embed(color=discord.Colour.red())
        msg: str = f"♥  **{lover.display_name}**, You have been asked in marriage by **{user.display_name}**.\n" \
                   f"If you wish to accept, type `yes`. Otherwise type anything else..."
        em.description = msg
        return em

    @staticmethod
    async def is_married(user: discord.Member) -> discord.Embed:
        em = discord.Embed(color=discord.Colour.blurple())
        msg: str = f"♥️ {user.display_name} is already married !"
        em.description = msg
        return em

    @staticmethod
    async def said_yes(user: discord.Member, lover: discord.Member) -> discord.Embed:
        em = discord.Embed(color=discord.Colour.blurple())
        msg: str = f"♥️ By the power of your love and commitment, " \
                   f"and the power vested in me, {lover.display_name} and {user.display_name}, " \
                   f"I now pronounce you married! You may kiss each other!"
        em.description = msg
        return em

    @staticmethod
    async def divorce(user: discord.Member, lover: discord.User) -> discord.Embed:
        em = discord.Embed(color=discord.Colour.red())
        msg: str = f"{user.name}#{user.discriminator}, you're now divorced from {lover.name}#{user.discriminator}"
        em.description = msg
        return em

    @staticmethod
    async def said_no(user: discord.Member, lover: discord.Member) -> discord.Embed:
        em = discord.Embed(color=discord.Colour.blurple())
        msg: str = f"I'm sorry {user.display_name} but {lover.display_name} said no...\n" \
                   f"Remember never to give up because you'll find the right person ! "
        em.description = msg
        return em

    @staticmethod
    async def already_married(user: discord.Member) -> discord.Embed:
        em = discord.Embed(color=discord.Colour.teal())
        msg: str = f"{user.display_name}, you are already married !"
        em.description = msg
        return em

    @staticmethod
    async def is_not_married(user: discord.Member) -> discord.Embed:
        em = discord.Embed(color=discord.Colour.orange())
        msg: str = f"{user.display_name} is not married yet !"
        em.description = msg
        return em
