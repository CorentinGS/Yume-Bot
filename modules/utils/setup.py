from modules.utils.db import Settings


class Setup:

	@staticmethod
	async def new_guild(guild_id:int):

		set = await Settings().get_server_settings(str(guild_id))

		set['Greet'] = False
		set['bl'] = False
		set['logging'] = False
		set['GreetChannel'] = None
		set['LogChannel'] = None
		set['automod'] = False
		set['Mute'] = []
		set['Display'] = False
		set['category'] = None
		set['Admins'] = []
		set['Mods'] = []
		set['Setup'] = False

		await Settings().set_server_settings(str(guild_id), set)


