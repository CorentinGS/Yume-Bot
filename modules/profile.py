import discord
from discord.ext import commands
import datetime
import asyncio

from modules.utils.db import Settings
from modules.utils.format import Embeds
from modules.utils import checks


class Profile:
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.group()
    async def profile(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.get, ctx.message.author)


    @profile.command()
    async def get(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.message.author

        if not await Settings().get_user_settings(str(user.id)):
            await ctx.invoke(self.default, user)

        set = await Settings().get_user_settings(str(user.id))
        glob = await Settings().get_glob_settings()


        if user.id in glob["VIP"]:
            vip = True
        else:
            vip = False

        gender = set['gender']

        em = await Embeds().format_get_profile_embed(ctx, user, vip, gender)
        await ctx.send(embed= em)

        return

    @profile.command()
    async def edit(self, ctx):

        auth = ctx.message.author

        set = await Settings().get_user_settings(str(auth.id))
        glob = await Settings().get_glob_settings()


        if auth.id in glob["VIP"]:
            vip = True
        else:
            vip = False

        em = await Embeds().format_profile_embed(ctx, auth, 'edit', vip)


        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji)

        msg = await ctx.send(embed=em)
        reactions = ["❓", '❌']
        for reaction in reactions:
            await msg.add_reaction(reaction)

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)

        except asyncio.TimeoutError:
            await ctx.send('👎')

        else:
            if reaction.emoji == '❓':
                await msg.clear_reactions()
                em = await Embeds().format_profile_embed(ctx, auth, 'gender', vip)
                await msg.edit(embed=em)
                reactions = ['👦', '👩', '💥', '🐌', '❌']
                if vip is True:
                    reactions.extend(['🐧', '🐱'])
                for reaction in reactions:
                    await msg.add_reaction(reaction)
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)

                except asyncio.TimeoutError:
                    await ctx.send('👎')

                else:
                    if reaction.emoji == '👦':
                        arg = "male"
                        await ctx.invoke(self.gender, arg)
                        await msg.delete()
                        await ctx.invoke(self.edit)
                    elif reaction.emoji == '👩':
                        arg = "female"
                        await ctx.invoke(self.gender, arg)
                        await msg.delete()
                        await ctx.invoke(self.edit)
                    elif reaction.emoji == '💥':
                        arg = "transgender"
                        await ctx.invoke(self.gender, arg)
                        await msg.delete()
                        await ctx.invoke(self.edit)
                    elif reaction.emoji == '🐌':
                        arg = "non-binary"
                        await ctx.invoke(self.gender, arg)
                        await msg.delete()
                        await ctx.invoke(self.edit)
                    elif reaction.emoji == '🐧':
                        arg = 'penguin'
                        await ctx.invoke(self.gender, arg)
                        await msg.delete()
                        await ctx.invoke(self.edit)
                    elif reaction.emoji == '🐱':
                        arg = 'cat'
                        await ctx.invoke(self.gender, arg)
                        await msg.delete()
                        await ctx.invoke(self.edit)
                    elif reaction.emoji == '❌':
                        await msg.delete()
                        return

            elif reaction.emoji == '❌':
                await msg.delete()
                return

    @profile.command()
    async def gender(self, ctx, arg: str = None):
        auth = str(ctx.message.author.id)
        set = await Settings().get_user_settings(auth)

        if arg.lower().startswith('male'):
            set['gender'] = "male"
        elif arg.lower().startswith('female'):
            set['gender'] = "female"
        elif arg.lower().startswith('trans'):
            set['gender'] = "transgender"
        elif arg.lower().startswith('cat'):
            set['gender'] = "cat"
        elif arg.lower().startswith('non-binary'):
            set['gender'] = "non-binary"
        elif arg.lower().startswith('penguin'):
            set['gender'] = 'penguin'
        elif arg.lowder().startswith('?'):
            set['gender'] = 'unknown'
        else:
            return await ctx.send(f'{arg} is not a valid argument !')

        await Settings().set_user_settings(auth, set)

    @profile.command()
    async def info(self, ctx, user: discord.Member = None):
        if user is None:
            auth = str(ctx.message.author.id)
        else:
            auth = str(user.id)
        set = await Settings().get_user_settings(auth)

        # TODO: Afficher les informations de qqun

    @profile.command()
    @checks.is_owner()
    async def setup(self, ctx):
        for guild in self.bot.guilds:
            for user in guild.members:
                set = await Settings().get_user_settings(str(user.id))
                set['gender'] = 'unknown'
                await Settings().set_user_settings(str(user.id), set)

    @profile.command()
    async def default(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.message.author

        if not await Settings().get_user_settings(str(user.id)):
            set = await Settings().get_user_settings(str(user.id))
            set['gender'] = 'unknown'
            await Settings().set_user_settings(str(user.id), set)

        else:
            return


def setup(bot):
    bot.add_cog(Profile(bot))
