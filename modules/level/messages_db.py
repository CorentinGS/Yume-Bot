from modules.sql.dbConnect import Db

class Message:

    def __init__(self, message_id: int, guild_id: int, channel_id: int, user_id: int, time_id: int):
        self.message_id = message_id
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.user_id = user_id
        self.time_id = time_id


class MessageDB:

    @staticmethod
    def insert_message(message: Message):

        try:
            con, meta = Db.connect()
            messages = meta.tables['messages']
            clause = messages.insert().values(
                message_id=message.message_id,
                guild_id=message.guild_id,
                channel_id=message.channel_id,
                user_id=message.user_id,
                time_id=message.time_id)
            con.execute(clause)
        except Exception as err:
            print(err)