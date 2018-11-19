import discord
from discord.ext import commands

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
                role = discord.utils.get(member.guild.roles, name="Muted")
                if role:
                    await member.add_roles(role)
                else:
                    pass
            else:
                pass

        if 'Blacklist' in glob:
            if member.id in glob['Blacklist']:
                if server["bl"] is True:
                    await guild.ban(member, reason="Blacklist")
                    #await member.send("you're in the blacklist ! If you think it's an error, ask here --> yumenetwork@protonmail.com")
                else:
                    pass
            else:
                pass

        if 'Greet' in server:
            if server['Greet'] is True:
                if 'GreetChannel' in server:
                    channel = self.bot.get_channel(int(server['GreetChannel']))
                    await channel.send('Welcome {} in {}'.format(member.mention, guild.name))
                    # TODO: Add embed format !
                else:
                    pass
            else:
                pass


    async def on_message(self, message):
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

                    else:
                        pass

        elif 'discord.gg/' in message.content:
            await message.delete()

        elif len(message.mentions) > 5:
            await message.delete()
            
    async def on_guild_join(self, guild):
        server = str(guild.id)
        set = await Settings().get_server_settings(server)
        if 'muteRole' not in set:
            set['muteRole'] = False
        if 'mute' not in set:
            set['mute'] = []
        if 'Greet' not in set:
            set['Greet'] = False
        await Settings().set_server_settings(server, set)



def setup(bot):
    bot.add_cog(Event(bot))
