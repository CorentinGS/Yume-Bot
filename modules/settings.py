import discord
from discord.ext import commands
import datetime
import asyncio

from modules.utils.db import Settings
from modules.utils.format import Embeds


class Set:

    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.group()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def setting(self, ctx):
        if ctx.invoked_subcommand is None:
            guild = ctx.message.guild
            em = await Embeds().format_set_embed(ctx, guild, 'setting')

            def check(reaction, user):
                return user == ctx.message.author and str(reaction.emoji)

            def msgcheck(m):
                if m.author == ctx.message.author:
                    return True
                else:
                    return False
            msg = await ctx.send(embed=em)
            reactions = ['🇲', '🇬', '❌']
            for reaction in reactions:
                await msg.add_reaction(reaction)

            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)

            except asyncio.TimeoutError:
                await ctx.send('👎')

            else:
                if reaction.emoji == '🇲':
                    await msg.clear_reactions()
                    em = await Embeds().format_set_embed(ctx, guild, 'mutemenu')
                    await msg.edit(embed=em)
                    reactions = ['💂', '💣', '❌']
                    for reaction in reactions:
                        await msg.add_reaction(reaction)
                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)

                    except asyncio.TimeoutError:
                        await ctx.send('👎')

                    else:
                        if reaction.emoji == '💂':
                            arg = "on"
                            await ctx.invoke(self.muterole, arg)
                            await msg.delete()
                            await ctx.invoke(self.setting)
                        elif reaction.emoji == '💣':
                            arg = "off"
                            await ctx.invoke(self.muterole, arg)
                            await msg.delete()
                            await ctx.invoke(self.setting)
                        elif reaction.emoji == '❌':
                            await msg.delete()
                            return

                if reaction.emoji == '🇬':
                    await msg.clear_reactions()
                    em = await Embeds().format_set_embed(ctx, guild, 'greetmenu')
                    await msg.edit(embed=em)
                    reactions = ['❔', '📜', '❌']
                    for reaction in reactions:
                        await msg.add_reaction(reaction)
                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)

                    except asyncio.TimeoutError:
                        await ctx.send('👎')

                    else:
                        if reaction.emoji == '❔':
                            await msg.delete()
                            await ctx.send('Please name a Channel !')
                            m = await self.bot.wait_for('message', timeout=60.0, check=msgcheck)
                            text_channel = discord.utils.get(
                                ctx.guild.text_channels, name=m.content)
                            await ctx.invoke(self.greetchannel, text_channel)
                            await ctx.invoke(self.setting)
                        elif reaction.emoji == '📜':
                            arg = "on"
                            await ctx.invoke(self.greet, arg)
                            await msg.delete()
                            await ctx.invoke(self.setting)
                        elif reaction.emoji == '❌':
                            await msg.delete()
                            return

                elif reaction.emoji == '❌':
                    await msg.delete()
                    return

    @setting.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def muterole(self, ctx, arg: str = None):
        server = str(ctx.guild.id)
        set = await Settings().get_server_settings(server)
        if arg.lower().startswith('on'):
            set['muteRole'] = True
        elif arg.lower().startswith('off'):
            set['muteRole'] = False
        else:
            return await ctx.send(f'{arg} is not a valid argument ! Please use **ON** or **OFF**')
        await Settings().set_server_settings(server, set)

        await ctx.send('OK !', delete_after=5)

    @setting.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def greetchannel(self, ctx, channel: discord.TextChannel):
        server = str(ctx.guild.id)
        set = await Settings().get_server_settings(server)

        if not channel:
            return await ctx.send('Invalid Channel')

        else:
            set['GreetChannel'] = int(channel.id)

        await Settings().set_server_settings(server, set)

        await ctx.send('OK !', delete_after=5)

    @setting.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def greet(self, ctx, arg: str = None):
        server = str(ctx.guild.id)
        set = await Settings().get_server_settings(server)
        if arg.lower().startswith('on'):
            set['Greet'] = True
        elif arg.lower().startswith('off'):
            set['Greet'] = False
        else:
            return await ctx.send(f'{arg} is not a valid argument ! Please use **ON** or **OFF**')

        await Settings().set_server_settings(server, set)

        await ctx.send('OK !', delete_after=5)


def setup(bot):
    bot.add_cog(Set(bot))
