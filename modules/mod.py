import discord
from discord.ext import commands
import json
import datetime
from itertools import cycle
import asyncio
import pymongo
from pymongo import MongoClient

class Mod:

    conf = {}

    def __init__(self, client, config):
        self.client = client
        self.config = config

        global conf
        conf = config

        global mongo
        global db
        mongo = MongoClient('mongo', 27017)
        db = mongo.bot


    @commands.command(pass_context = True)
    @commands.guild_only()
    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.has_permissions(manage_messages = True)
    async def mute(self, ctx, user: discord.Member, duration, *,  reason: str = None):

        role = discord.utils.get(ctx.guild.roles, name="Muted")
        msg = ctx.message
        server = ctx.guild.name
        id = user.id



        unit = duration[-1]
        if unit == 's':
            time = int(duration[:-1])
            longunit = 'seconds'
        elif unit == 'm':
            time = int(duration[:-1]) * 60
            longunit = 'minutes'
        elif unit == 'h':
            time = int(duration[:-1]) * 3600
            longunit = 'hours'
        else:
            await ctx.send('Invalid Unit! Use `s`, `m`, or `h`.')
            return

        db[server].update_one(
            {
                'User_id' : id
            },
            {
                '$set': {
                    'Name' : '{}#{}'.format(user.name, user.discriminator),
                    'User_id': user.id,

                    'Mute': True,
                    'Time' : time,
                    'Reason': reason
                    }
            },
            True
        )

        try:
            await msg.delete()
            await user.add_roles(role)

            await ctx.send('{} has been muted for {} with the reason : {}.'.format(user.mention, duration, reason))

        except:
            pass

        await asyncio.sleep(time)

        try:
            await user.remove_roles(role)
            db[server].update_one(
                {
                    'User_id' : id
                },
                {
                    '$set': {
                        'Name' : '{}#{}'.format(user.name, user.discriminator),
                        'User_id': user.id,

                        'Mute': False,
                        'Time' : None,
                        'Reason': None
                        }
                },
                True
            )

            return await ctx.send("{} has been unmuted".format(user.mention))


        except:
            pass

    @commands.command(pass_context = True)
    @commands.guild_only()
    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.has_permissions(manage_messages = True)
    async def unmute(self, ctx, user: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        msg = ctx.message
        server = ctx.guild.name
        id = user.id

        await user.remove_roles(role)
        await msg.delete()
        db[server].update_one(
            {
                'User_id' : id
            },
            {
                '$set': {
                    'Name' : '{}#{}'.format(user.name, user.discriminator),
                    'User_id': user.id,

                    'Mute': False,
                    'Time' : None,
                    'Reason': None
                    }
            },
            True
        )

        return await ctx.send("{} has been unmuted".format(user.display_name))


    @commands.command(pass_context = True)
    @commands.guild_only()
    @commands.cooldown(2, 20, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = None):

        msg = ctx.message
        server = ctx.guild
        moderator = ctx.message.author

        try:
            await ctx.guild.kick(member)

        except discord.Forbidden:
            return await ctx.send('Forbidden')


        embed = discord.Embed(
            title="Kick",
            description="The KickHammer stroke someone...",
            color = discord.Colour.dark_red()
        )

        embed.add_field(name="Name", value="{}#{}".format(member.name, member.discriminator), inline=True)
        embed.add_field(name="Created at", value=member.created_at.strftime('%A - %B - %e - %g at %H:%M'), inline=True)
        embed.add_field(name="Kicked at", value=datetime.datetime.now().strftime('%A - %B - %e - %g at %H:%M'), inline=True)
        embed.add_field(name="ID", value=id, inline=True)
        embed.add_field(name="Reason", value=reason, inline=True)
        embed.add_field(name="Mod", value=moderator, inline=True)
        embed.set_thumbnail(url=member.avatar_url)

        await msg.delete()
        await ctx.send(embed=embed)
        return

    @commands.command(pass_context = True)
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(ban_members = True)
    async def hackban(self, ctx, id: int, *, reason: str = None):

        server = ctx.guild
        msg = ctx.message
        moderator = ctx.message.author
        member = discord.Object(id=id)


        try:
            await ctx.guild.ban(member)


        except discord.Forbidden:
            return await ctx.send("Forbidden")


        banned = await self.client.get_user_info(id)

        embed = discord.Embed(
            title="Hackban",
            description="The BanHammer stroke someone...",
            color = discord.Colour.dark_red()
        )

        embed.add_field(name="Name", value="{}#{}".format(banned.name, banned.discriminator), inline=True)
        embed.add_field(name="Created at", value=banned.created_at.strftime('%A - %B - %e - %g at %H:%M'), inline=True)
        embed.add_field(name="Banned at", value=datetime.datetime.now().strftime('%A - %B - %e - %g at %H:%M'), inline=True)
        embed.add_field(name="ID", value=id, inline=True)
        embed.add_field(name="Reason", value=reason, inline=True)
        embed.add_field(name="Mod", value=moderator, inline=True)
        embed.set_thumbnail(url=banned.avatar_url)

        await msg.delete()
        await ctx.send(embed=embed)
        return


        @commands.command(pass_context = True)
        @commands.guild_only()
        @commands.cooldown(2, 10, commands.BucketType.user)
        @commands.has_permissions(ban_members = True)
        async def unban(self, ctx, id: int):

            server = ctx.guild
            msg = ctx.message
            moderator = ctx.message.author
            member = discord.Object(id=id)


            try:
                await ctx.guild.unban(member)

            except:
                pass

    @commands.command(pass_context = True)
    @commands.guild_only()
    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, user: discord.Member, *, reason: str = None):

        server = ctx.guild
        msg = ctx.message
        moderator = ctx.message.author
        id = user.id

        try:
            await ctx.guild.ban(user, reason = reason, delete_message_days=7)

        except discord.Forbidden:
            return await ctx.send("Forbidden")

        except discord.HTTPException:
            return await ctx.send("HTTPException")



        embed = discord.Embed(
            title="Ban",
            description="The BanHammer stroke someone...",
            color = discord.Colour.dark_red()
        )

        embed.add_field(name="Name", value="{}#{}".format(user.name, user.discriminator), inline=True)
        embed.add_field(name="Created at", value=user.created_at.strftime('%A - %B - %e - %g at %H:%M'), inline=True)
        embed.add_field(name="Banned at", value=datetime.datetime.now().strftime('%A - %B - %e - %g at %H:%M'), inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Reason", value=reason, inline=True)
        embed.add_field(name="Mod", value=moderator, inline=True)
        embed.set_thumbnail(url=user.avatar_url)

        await msg.delete()
        await ctx.send(embed=embed)
        return

    @commands.command(pass_context = True)
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    @commands.cooldown(2, 10, commands.BucketType.user)
    async def purge(self,ctx, amount: int):

        msg = ctx.message

        try:
            await msg.delete()
            return await ctx.channel.purge(limit=amount + 1)

        except:
            pass



def setup(client):
    client.add_cog(Mod(client, client.config))
