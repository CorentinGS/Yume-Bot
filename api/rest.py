from db import Settings as db
from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    set = db().get_key_settings(str(username))
    if not set:
        return None
    else:
        return set[str('key')]


@auth.error_handler
def unauthorized():
    return 'Not authorized', 404


class Global(Resource):

    @auth.login_required
    def get(self):
        set = db().get_glob_settings()
        return set, 200

    @staticmethod
    def put():
        parser = reqparse.RequestParser()
        parser.add_argument('VIP')
        args = parser.parse_args()
        set = db().get_glob_settings
        set["VIP"] = args['VIP']
        db().set_glob_settings(set)


class Guild(Resource):

    @auth.login_required
    def get(self, id):

        if not db().get_server_settings(str(id)):
            return 'Guild not found', 404
        else:
            set = db().get_server_settings(str(id))
            return set, 200

    @staticmethod
    def put(id):
        parser = reqparse.RequestParser()

        # bool

        parser.add_argument('Greet') # | Message de bienvenue
        parser.add_argument('bl') # | Activation de la Blacklsit
        parser.add_argument('logging') # | Activation du logging
        parser.add_argument("automod") # | Activation de l'automodération

        # Integer
        parser.add_argument('GreetChannel') # | Salon de bienvenue
        parser.add_argument('LogChannel') # | Salon de logging

        # List
        parser.add_argument('Mods') # | Rôles de modération
        parser.add_argument('Admins') # | Rôles d'administration

        args = parser.parse_args()

        set = db().get_user_settings(str(id))
        set["Greet"] = args['Greet']
        set['bl'] = args['bl']
        set['logging'] = args['logging']
        set['automod'] = args['automod']
        set['GreetChannel'] = args['GreetChannel']
        set['LogChannel'] = args['LogChannel']
        for admin in args["Admins"]:
            set['Admins'].append(admin)
        for mod in args["Mods"]:
            set['Mods'].append(mod)
        db().set_server_settings(str(id), set)

        return set, 201


class Level(Resource):

    @auth.login_required
    def get(self, id):

        if not db().get_server_settings(str(id)):
            return 'Guild not found', 404
        else:
            set = db().get_server_settings(str(id))
            return set, 200


api.add_resource(Guild, "/guild/<string:id>")
api.add_resource(Global, "/global")
api.add_resource(Level, "/level/<string:id>")

app.run(host='0.0.0.0', port=4437, debug=True)
