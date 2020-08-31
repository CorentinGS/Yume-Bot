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
        con, cur = Db.connect()
        try:
            cur.execute(
                "INSERT INTO public.messages (  message_id, guild_id, channel_id, user_id, time_id) \
                VALUES ( %s::text, %s::text, %s::text, %s::text, %s );", (
                    str(message.message_id), str(message.guild_id), str(message.channel_id), str(message.user_id),
                    message.time_id))
        except Exception as err:
            print(err)
            con.rollback()
        con.commit()
