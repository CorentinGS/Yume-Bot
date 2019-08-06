from discord.ext import commands


class ModReason(commands.Converter):
	async def convert(self, ctx, arg):
		if len(arg) > 256:
			raise commands.BadArgument(f'the reason is too long ! The limit is 256char!)')
		return arg


class MemberID(commands.Converter):
	async def convert(self, ctx, arg):
		try:
			m = await commands.MemberConverter().convert(ctx, arg)
		except commands.BadArgument:
			try:
				return int(arg, base=10)
			except ValueError:
				raise commands.BadArgument(f"{arg} is not a valid member or member ID.") from None
		else:
			return m.id
