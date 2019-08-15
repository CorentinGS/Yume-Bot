import discord


class Utils:

	@staticmethod
	async def delete_voice_chan(ctx, id: int):
		try:
			chan = discord.utils.get(ctx.guild.voice_channels, id=id)
			await chan.delete()
		except discord.NotFound:
			return
		except discord.Forbidden:
			return await ctx.send("I need more permissions to be able to to that", delete_after=5)

	@staticmethod
	async def delete_text_chan(ctx, id: int):
		try:
			chan = discord.utils.get(ctx.guild.text_channels, id=id)
			await chan.delete()
		except discord.NotFound:
			return
		except discord.Forbidden:
			return await ctx.send("I need more permissions to be able to to that", delete_after=5)
