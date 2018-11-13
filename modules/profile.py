import discord
from discord.ext import commands
import datetime
import asyncio

from modules.utils.db import Settings
from modules.utils.format import Embeds



class Profile:
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.group()
    async def profile(self, ctx):
        if ctx.invoked_subcommand is None:

            glob = await Settings().get_glob_settings()

            auth = ctx.message.author

            if auth.id in glob["VIP"]:
                vip = True
            else:
                vip = False

            em = await Embeds().format_profile_embed(ctx, auth, 'profile', vip)


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
                            await ctx.invoke(self.profile)
                        elif reaction.emoji == '👩':
                            arg = "female"
                            await ctx.invoke(self.gender, arg)
                            await msg.delete()
                            await ctx.invoke(self.profile)
                        elif reaction.emoji == '💥':
                            arg = "transgender"
                            await ctx.invoke(self.gender, arg)
                            await msg.delete()
                            await ctx.invoke(self.profile)
                        elif reaction.emoji == '🐌':
                            arg = "non-binary"
                            await ctx.invoke(self.gender, arg)
                            await msg.delete()
                            await ctx.invoke(self.profile)
                        elif reaction.emoji == '🐧':
                            arg = 'penguin'
                            await ctx.invoke(self.gender, arg)
                            await msg.delete()
                            await ctx.invoke(self.profile)
                        elif reaction.emoji == '🐱':
                            arg = 'cat'
                            await ctx.invoke(self.gender, arg)
                            await msg.delete()
                            await ctx.invoke(self.profile)
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

def setup(bot):
    bot.add_cog(Profile(bot))
