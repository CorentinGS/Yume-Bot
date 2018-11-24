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
            vip = False

            guild = ctx.message.guild
            set = await Settings().get_server_settings(str(guild.id))
            em = await Embeds().format_set_embed(ctx, guild, 'setting', vip)
            glob = await Settings().get_glob_settings()

            def check(reaction, user):
                return user == ctx.message.author and str(reaction.emoji)

            def msgcheck(m):
                if m.author == ctx.message.author:
                    return True
                else:
                    return False

            msg = await ctx.send(embed=em)
            reactions = ['🇲', '🇬', '⛔', '🖊', '🔨', '❌']
            for reaction in reactions:
                await msg.add_reaction(reaction)

            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)

            except asyncio.TimeoutError:
                await ctx.send('👎')

            else:
                if reaction.emoji == '🇲':
                    await msg.clear_reactions()
                    em = await Embeds().format_set_embed(ctx, guild, 'mutemenu', vip)
                    await msg.edit(embed=em)
                    reactions = ['💂', '💣', '❌']
                    for reaction in reactions:
                        await msg.add_reaction(reaction)
                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)

                    except asyncio.TimeoutError:
                        await ctx.send('👎', delete_after=10)

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

                elif reaction.emoji == '🔨':
                    await msg.clear_reactions()
                    if ctx.message.author in glob["VIP"]:
                        vip = True
                    em = await Embeds().format_set_embed(ctx, guild, 'automenu', vip)
                    await msg.edit(embed=em)
                    reactions = ['✅', '🚫', '❌']
                    if vip is True:
                        reactions.extend(['⛔'])
                    for reaction in reactions:
                        await msg.add_reaction(reaction)

                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)

                    except asyncio.TimeoutError:
                        await ctx.send('👎', delete_after=10)

                    else:
                        if reaction.emoji == '✅':
                            set["automod"] = True
                            await msg.delete()
                            await Settings().set_server_settings(str(guild.id), set)
                            await ctx.invoke(self.setting)
                        elif reaction.emoji == '🚫':
                            set['automod'] = False
                            await msg.delete()
                            await Settings().set_server_settings(str(guild.id), set)
                            await ctx.invoke(self.setting)
                        elif reaction.emoji == '⛔':
                            await msg.delete()
                            await ctx.send("Not ready ! Ccoming Soon")
                            await ctx.invoke(self.setting)
                        elif reaction.emoji == '❌':
                            await msg.delete()
                            return



                elif reaction.emoji == '🖊':
                    if ctx.message.author in glob["VIP"]:
                        vip = True

                    await msg.clear_reactions()
                    em = await Embeds().format_set_embed(ctx, guild, 'loggingmenu', vip)
                    await msg.edit(embed=em)
                    reactions = ['📋', '🆓', '❔', '❌']
                    '''
                    if vip is True:
                        reactions.extend(['🎬'])
                    '''
                    for reaction in reactions:
                        await msg.add_reaction(reaction)
                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=120)

                    except asyncio.TimeoutError:
                        await ctx.send('👎')

                    else:
                        if reaction.emoji == '📋':
                            arg = "on"
                            await ctx.invoke(self.logging, arg)
                            await msg.delete()
                            await ctx.invoke(self.setting)
                        elif reaction.emoji == '🆓':
                            arg = 'off'
                            await ctx.invoke(self.logging, arg)
                            await msg.delete()
                            await ctx.invoke(self.setting)
                        elif reaction.emoji == '❔':
                            await msg.delete()
                            await ctx.send('Please name a Channel !')
                            m = await self.bot.wait_for('message', timeout=60.0, check=msgcheck)
                            text_channel = m.channel_mentions[0]
                            await ctx.invoke(self.loggingchannel, text_channel)
                            await ctx.invoke(self.setting)
                        elif reaction.emoji == '❌':
                            await msg.delete()
                            return
                elif reaction.emoji == '⛔':
                    await msg.clear_reactions()
                    em = await Embeds().format_set_embed(ctx, guild, 'blacklistmenu', vip)
                    await msg.edit(embed = em)
                    reactions = ['🚫', '🔓', '❌']
                    for reaction in reactions:
                        await msg.add_reaction(reaction)
                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)

                    except asyncio.TimeoutError:
                        await ctx.send('👎')

                    else:
                        if reaction.emoji == '🚫':
                            arg = True
                            await ctx.invoke(self.bl, arg)
                            await msg.delete()
                            await ctx.invoke(self.setting)
                        elif reaction.emoji == '🔓':
                            arg = False
                            await ctx.invoke(self.bl, arg)
                            await msg.delete()
                            await ctx.invoke(self.setting)
                        elif reaction.emoji == '❌':
                            await msg.delete()
                            return

                elif reaction.emoji == '🇬':
                    await msg.clear_reactions()
                    em = await Embeds().format_set_embed(ctx, guild, 'greetmenu', vip)
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
                            text_channel = m.channel_mentions[0]
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
    async def logging(self, ctx, arg: str = None):
        server = str(ctx.guild.id)
        set = await Settings().get_server_settings(server)
        if arg.lower().startswith('on'):
            set['logging'] = True
        elif arg.lower().startswith('off'):
            set['logging'] = False
        else:
            return await ctx.send(f'{arg} is not a valid argument ! Please use **ON** or **OFF**')
        await Settings().set_server_settings(server, set)

        await ctx.send('OK !', delete_after=5)

    @setting.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def loggingchannel(self, ctx, channel: discord.TextChannel):
        server = str(ctx.guild.id)
        set = await Settings().get_server_settings(server)

        if not channel:
            return await ctx.send('Invalid Channel')

        else:
            set['LogChannel'] = int(channel.id)

        await Settings().set_server_settings(server, set)

        await ctx.send('OK !', delete_after=5)

    @setting.command()
    @commands.has_permissions(administrator = True)
    async def bl(self, ctx, arg: bool = False):
        server = str(ctx.guild.id)
        set = await Settings().get_server_settings(server)
        if arg is True:
            set['bl'] = True
        else:
            set['bl'] = False
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
