import discord
from discord.ext import commands


class Utilities:

    conf = {}

    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

        global conf
        conf = config

    @commands.command(aliases=["server"])
    @commands.guild_only()
    #  @commands.cooldown(1, 60, commands.BucketType.guild)
    async def info(self, ctx):
        msg = ctx.message
        server = ctx.message.guild

        if server.mfa_level == 1:
            af = "True"

        else:
            af = "False"

        embed = discord.Embed(
            title="{}".format(ctx.message.guild.name),
            description="I found this...",
            color=discord.Colour.dark_gold()
        )

        embed.add_field(name="Name", value=server.name, inline=True)
        embed.add_field(name="ID", value=server.id, inline=True)
        embed.add_field(name="Roles", value=len(server.roles), inline=True)
        embed.add_field(name="Members", value=len(
            server.members), inline=True)
        embed.add_field(name="Channels", value=len(
            server.channels), inline=True)
        embed.add_field(name="Security",
                        value=server.verification_level, inline=True)
        embed.add_field(name="Region", value=server.region, inline=True)
        embed.add_field(name="Owner", value=server.owner, inline=True)
        embed.add_field(name="2AF", value=af, inline=False)
        embed.add_field(name="created at", value=server.created_at.strftime(
            '%A - %B - %e at %H:%M'), inline=False)
        embed.set_thumbnail(url=server.icon_url)

        try:
            await msg.delete()
            return await ctx.send(embed=embed)

        except discord.HTTPException:
            pass

    @commands.command()
    @commands.guild_only()
    async def roleinfo(self, ctx, *, role: discord.Role):
        color = role.colour

        embed = discord.Embed(colour=color)

        embed.set_author(name=role.name)
        embed.add_field(name="Users", value=len(role.members))
        embed.add_field(name="Hoist", value=role.hoist)
        embed.add_field(name="Position", value=role.position)
        embed.set_footer(text=f'Role ID: {role.id}')

        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    #  @commands.cooldown(1, 60, commands.BucketType.guild)
    async def members(self, ctx):
        msg = ctx.message
        server = ctx.message.guild

        embed = discord.Embed(
            title="{}".format(ctx.message.guild.name),
            description="I found this...",
            color=discord.Colour.dark_gold()
        )

        embed.add_field(name="Members", value=len(
            server.members), inline=True)
        embed.set_thumbnail(url=server.icon_url)

        try:
            await msg.delete()
            return await ctx.send(embed=embed)

        except discord.HTTPException:
            pass

    @commands.command()
    @commands.guild_only()
    #  @commands.cooldown(1, 60, commands.BucketType.guild)
    async def owner(self, ctx):
        msg = ctx.message
        server = ctx.message.guild

        embed = discord.Embed(
            title="{}".format(ctx.message.guild.name),
            description="I found this...",
            color=discord.Colour.dark_gold()
        )

        embed.add_field(name="Owner", value=server.owner.mention, inline=True)
        embed.set_thumbnail(url=server.icon_url)

        try:
            await msg.delete()
            return await ctx.send(embed=embed)

        except discord.HTTPException:
            pass

    @commands.command()
    @commands.guild_only()
    #  @commands.cooldown(1, 20, commands.BucketType.user)
    async def avatar(self, ctx, *, user: discord.Member = None):

        if user is None:
            user = ctx.author

        return await ctx.send(f"Avatar of {user.name} \n {user.avatar_url_as(size=1024)}")

    @commands.command()
    @commands.guild_only()
    #  @commands.cooldown(1, 120, commands.BucketType.guild)
    async def icon(self, ctx):
        return await ctx.send(f"Icon of {ctx.guild.name}\n{ctx.guild.icon_url_as(size=1024)}")

    @commands.command()
    @commands.guild_only()
    #  @commands.cooldown(2, 20, commands.BucketType.user)
    async def whois(self, ctx, user: discord.Member):

        msg = ctx.message

        embed = discord.Embed(
            title="{}".format(user.name),
            description="I found this...",
            color=discord.Colour.magenta()
        )

        embed.add_field(name="Name", value="{}#{}".format(
            user.name, user.discriminator), inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Status", value=user.status, inline=True)
        embed.add_field(name="Hightest role", value=user.top_role, inline=True)
        embed.add_field(name="Joined", value=user.joined_at.strftime(
            '%A - %B - %e - %g at %H:%M'), inline=True)
        embed.add_field(name="Nick", value=user.nick, inline=True)
        embed.add_field(name="Created", value=user.created_at.strftime(
            '%A - %B - %e - %g at %H:%M'), inline=True)
        embed.add_field(name="Mention", value=user.mention, inline=True)
        embed.set_thumbnail(url=user.avatar_url)

        try:
            await msg.delete()
            return await ctx.send(embed=embed)

        except discord.HTTPException:
            pass

    @commands.command()
    @commands.guild_only()
    #  @commands.cooldown(2, 20, commands.BucketType.user)
    async def hackwhois(self, ctx, id: int):

        user = await self.bot.get_user_info(id)
        msg = ctx.message

        embed = discord.Embed(
            title="{}".format(user.name),
            description="I found this...",
            color=discord.Colour.magenta()
        )

        embed.add_field(name="Name", value="{}#{}".format(
            user.name, user.discriminator), inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Created", value=user.created_at.strftime(
            '%A - %B - %e - %g at %H:%M'), inline=True)
        embed.set_thumbnail(url=user.avatar_url)

        try:
            await msg.delete()
            return await ctx.send(embed=embed)

        except discord.HTTPException:
            pass

    @commands.command()
    @commands.guild_only()
    async def invite(self, ctx):

        toto = await ctx.channel.create_invite(max_uses=15)
        await ctx.send(f"https://discord.gg/{toto.code}")


def setup(bot):
    bot.add_cog(Utilities(bot, bot.config))
