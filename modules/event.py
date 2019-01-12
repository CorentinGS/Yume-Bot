import random

import discord
from discord.ext import commands

from modules.utils import checks, lists
from modules.utils.db import Settings


class Event:

    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    async def on_member_join(self, member):
        guild = member.guild
        server = await Settings().get_server_settings(str(guild.id))
        glob = await Settings().get_glob_settings()
        if 'Mute' in server:
            if member.id in server['Mute']:
                for chan in guild.text_channels:
                    await chan.set_permissions(member, send_messages=False)
                if server['logging'] is True:
                    if 'LogChannel' in server:
                        channel = self.bot.get_channel(
                            int(server['LogChannel']))
                    else:
                        pass

            else:
                pass


        if 'Blacklist' in glob:
            if member.id in glob['Blacklist']:
                if server["bl"] is True:
                    await guild.ban(member, reason="Blacklist")
                    # await member.send("you're in the blacklist ! If you think it's an error, ask here --> yumenetwork@protonmail.com")
                else:
                    pass
            else:
                pass

        if 'Greet' in server:
            if server['Greet'] is True:
                if 'GreetChannel' in server:
                    channel = self.bot.get_channel(int(server['GreetChannel']))
                    greet = random.choice(lists.greet)

                    em = discord.Embed(timestamp=member.joined_at)
                    em.set_author(name="Welcome", icon_url=member.avatar_url)
                    em.set_footer(text=f'{member.name}')
                    em.description = f"{greet}"
                    await channel.send(embed=em)
                else:
                    pass
            else:
                pass

        if 'Display' in server:
            if server['Display'] is True:
                category = discord.utils.get(
                    member.guild.categories, id=int(server['category']))
                for channel in category.channels:
                    await channel.delete()

                overwrite = {
                    member.guild.default_role: discord.PermissionOverwrite(connect=False),
                } 
                    
                await member.guild.create_voice_channel(f'Users : {len(member.guild.members)}', overwrites = overwrite, category = category)
                bots = []
                for user in member.guild.members:
                    if user.bot is True:
                        bots.append(user)
                await member.guild.create_voice_channel(f'Bots : {len(bots)}', overwrites = overwrite, category = category)
                await member.guild.create_voice_channel(f'Members : {len(member.guild.members) - len(bots)}', overwrites = overwrite, category = category)


    async def on_member_remove(self, member):
        guild = member.guild
        server = await Settings().get_server_settings(str(guild.id))

        if 'Display' in server:
            if server['Display'] is True:
                category = discord.utils.get(
                    member.guild.categories, id=int(server['category']))
                for channel in category.channels:
                    await channel.delete()

                overwrite = {
                    member.guild.default_role: discord.PermissionOverwrite(connect=False),
                } 
                    
                await member.guild.create_voice_channel(f'Users : {len(member.guild.members)}', overwrites = overwrite, category = category)
                bots = []
                for user in member.guild.members:
                    if user.bot is True:
                        bots.append(user)
                await member.guild.create_voice_channel(f'Bots : {len(bots)}', overwrites = overwrite, category = category)
                await member.guild.create_voice_channel(f'Members : {len(member.guild.members) - len(bots)}', overwrites = overwrite, category = category)

        if 'Greet' in server:
            if server['Greet'] is True:
                if 'GreetChannel' in server:
                    channel = self.bot.get_channel(int(server['GreetChannel']))
                    leave = random.choice(lists.leave)

                    em = discord.Embed(timestamp=member.joined_at)
                    em.set_author(name="Left", icon_url=member.avatar_url)
                    em.set_footer(text=f'{member.name}')
                    em.description = f"{leave}"
                    await channel.send(embed=em)
                else:
                    pass
            else:
                pass
    async def on_message(self, message):
        server = await Settings().get_server_settings(str(message.guild.id))
        author = message.author
        glob = await Settings().get_glob_settings()
        if 'AFK' in glob:
            if author.id in glob['AFK']:
                if message.content is '--afk':
                    return
                glob['AFK'].remove(author.id)
                await Settings().set_glob_settings(glob)
                await message.channel.send("{}, welcome back !".format(author.mention), delete_after=10)
            else:
                for user in message.mentions:
                    if user.id in glob['AFK']:
                        await message.channel.send("{}#{} is AFK".format(user.name, user.discriminator), delete_after=10)
                        await user.send(f"{author} has mentionned you in {message.guild} : \n`{message.content}`")


        if server['automod'] == True:
            if not message.author == message.guild.owner:
                if 'discord.gg/' in message.content:
                    await message.delete()

                elif len(message.mentions) > 5:
                    await message.delete()
            else:
                pass

        else:
            pass

def setup(bot):
    bot.add_cog(Event(bot))
