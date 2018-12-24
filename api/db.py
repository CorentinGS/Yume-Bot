import pymongo

class Settings():

    def __init__(self):
        self.client = pymongo.MongoClient('127.0.0.1', 27017)

        self.db = self.client.bot

        self.glob = self.db.glob
        self.servers = self.db.servers
        self.profiles = self.db.profiles
        self.keys = self.db.keys


    def get_glob_settings(self):
        doc = self.glob.find_one({"_id": 0})
        return doc or {}

    def set_glob_settings(self, settings):
        return self.glob.replace_one({"_id": 0}, settings, True)

    def set_server_settings(self, id, settings):
        return self.servers.replace_one({"_id": id}, settings, True)

    def get_server_settings(self, id):
        doc = self.servers.find_one({"_id": id})
        return doc or {}

    def get_user_settings(self, id):
        doc =  self.profiles.find_one({"_id": id})
        return doc or {}

    def set_user_settings(self, id, settings):
        return self.profiles.replace_one({"_id": id}, settings, True)

    def get_key_settings(self, name):
        doc = self.keys.find_one({"_id" : name})
        return doc or {}
