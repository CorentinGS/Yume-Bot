import asyncio
import datetime

import discord
from discord.ext import commands

from modules.utils import checks
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
            await ctx.invoke(self.get, ctx.message.author)

    @profile.command()
    async def get(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.message.author

        set = await Settings().get_user_settings(str(user.id))
        glob = await Settings().get_glob_settings()

        if 'gender' not in set:
            set['gender'] = 'unknown'
        if 'status' not in set:
            set['status'] = 'alone'
        if 'lover' not in set:
            set['lover'] = user.id
        if 'desc' not in set:
            set['desc'] = "A discord user"
        if 'xp' not in set:
            set['xp'] = 0
        if 'level' not in set:
            set['level'] = 0
        if 'reach' not in set:
            set['reach'] = 0
        if 'vip' not in set:
            set['vip'] = False

        await Settings().set_user_settings(str(user.id), set)

        if user.id in glob["VIP"]:
            vip = True
        else:
            vip = False

        gender = set['gender']
        status = set['status']
        description = set['desc']
        lover = await self.bot.get_user_info(int(set['lover']))
        xp = set['xp']
        reach = set['reach']
        level = set['level']

        em = await Embeds().format_get_profile_embed(ctx, user, vip, gender, status, lover, description, xp, reach, level)

        reactions = ["✏", '❌']

        msg = await ctx.send(embed=em)

        if user == ctx.message.author:
            for reaction in reactions:
                await msg.add_reaction(reaction)

            def check(reaction, user):
                return user == ctx.message.author and str(reaction.emoji)

            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=240)

            except asyncio.TimeoutError:
                await ctx.send('👎', delete_after=10)

            else:
                if reaction.emoji == '✏':
                    await msg.clear_reactions()
                    await msg.delete()
                    await ctx.invoke(self.edit)
                if reaction.emoji == '❌':
                    await msg.clear_reactions()
                    await msg.delete()
                    return

    @profile.command()
    async def edit(self, ctx):
        auth = ctx.message.author

        glob = await Settings().get_glob_settings()

        if auth.id in glob["VIP"]:
            vip = True
        else:
            vip = False

        em = await Embeds().format_profile_embed(ctx, auth, 'edit', vip)

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji)

        msg = await ctx.send(embed=em)
        reactions = ["❓", '❤', '🖊', '❌']
        for reaction in reactions:
            await msg.add_reaction(reaction)

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)

        except asyncio.TimeoutError:
            await ctx.send('👎', delete_after=10)

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
                    await ctx.send('👎', delete_after=10)

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

            elif reaction.emoji == '❤':
                await msg.delete()
                await ctx.invoke(self.love)

            elif reaction.emoji == '🖊':
                await msg.delete()
                await ctx.invoke(self.desc)

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
    async def desc(self, ctx):
        user = ctx.message.author
        set = await Settings().get_user_settings(str(user.id))

        def msgcheck(m):
            if m.author == ctx.message.author:
                return True
            else:
                return False

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji)

        reactions = ['🖊', '❌']
        content = set['desc']

        em = await Embeds().format_desc_profile_embed(ctx, user, content)

        msg = await ctx.send(embed=em)

        for reaction in reactions:
            await msg.add_reaction(reaction)

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)

        except asyncio.TimeoutError:
            await ctx.send('👎', delete_after=10)

        if reaction.emoji == '🖊':
            await msg.delete()
            await ctx.send('Please ! Write your description', delete_after=380)

            try:
                m = await self.bot.wait_for('message', timeout=380.0, check=msgcheck)

            except asyncio.TimeoutError:
                await ctx.send('👎', delete_after=10)

            set['desc'] = m.content
            await Settings().set_user_settings(str(user.id), set)

        elif reaction.emoji == '❌':
            await msg.delete()
            return

    @commands.group()
    async def love(self, ctx):
        if ctx.invoked_subcommand is None:
            auth = ctx.message.author
            em = await Embeds().format_love_embed(ctx, auth, 'love')

            msg = await ctx.send(embed=em)
            reactions = ["💘", '❌']
            for reaction in reactions:
                await msg.add_reaction(reaction)

            def check(reaction, user):
                return user == ctx.message.author and str(reaction.emoji)

            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)

            except asyncio.TimeoutError:
                await ctx.send('👎', delete_after=10)

            else:
                if reaction.emoji == '💘':
                    await msg.delete()
                    await ctx.invoke(self.declaration)

                elif reaction.emoji == '❌':
                    await msg.delete()
                    return

    @love.command()
    async def declaration(self, ctx):
        await ctx.send('Please Mention the person you love !')

        def msgcheck(m):
            return m.author == ctx.message.author

        try:
            m = await self.bot.wait_for('message', timeout=60.0, check=msgcheck)

        except asyncio.TimeoutError:
            await ctx.send('👎', delete_after=10)

        else:
            toto = ctx.message.author
            user = m.mentions[0]

            em = await Embeds().format_love_embed(ctx, toto, 'declaration')
            reactions = ["✅", '❌']

            msg = await user.send(embed=em)
            for reaction in reactions:
                await msg.add_reaction(reaction)

            def check(reaction, member):
                return member == user and str(reaction.emoji)

            try:
                reaction, member = await self.bot.wait_for('reaction_add', check=check, timeout=86400)

            except asyncio.TimeoutError:
                await ctx.send('Too late', delete_after=10)

            else:
                if reaction.emoji == '✅':
                    set = await Settings().get_user_settings(str(user.id))

                    await user.send('OK')
                    await msg.delete()
                    await toto.send('{} said yes. <3'.format(user))

                    set['status'] = "taken"
                    set['lover'] = toto.id
                    await Settings().set_user_settings(str(user.id), set)

                    set = await Settings().get_user_settings(str(toto.id))
                    set['status'] = 'taken'
                    set['lover'] = user.id
                    await Settings().set_user_settings(str(toto.id), set)

                elif reaction.emoji == '❌':
                    await msg.delete()
                    return await toto.send('{} said no... :cry: !'.format(user))


def setup(bot):
    bot.add_cog(Profile(bot))
