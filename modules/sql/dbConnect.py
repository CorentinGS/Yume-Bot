import json

import sqlalchemy


class Db:

    @staticmethod
    def connect():
        with open("./config/keys.json", "r") as cjson:
            keys = json.load(cjson)

        url = 'postgresql://postgres:{}@postgre:5432/yumebot'.format(keys["postgresql"])

        # The return value of create_engine() is our connection object
        con = sqlalchemy.create_engine(url, client_encoding='utf8')

        # We then bind the connection to MetaData()
        meta = sqlalchemy.MetaData(bind=con, reflect=True)

        return con, meta
