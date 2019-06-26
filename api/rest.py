<<<<<<< HEAD
from db import Settings
from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api, Resource, reqparse
=======
from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api, Resource, reqparse

import api.db as db
>>>>>>> lg

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
	set = db.Settings().get_key_settings(str(username))
	if not set:
		return None
	else:
		return set[str('key')]


@auth.error_handler
def unauthorized():
	return 'Not authorized', 404


class Global(Resource):
<<<<<<< HEAD
    @auth.login_required
    def get(self, id):
        set = Settings().get_glob_settings
        return set, 200

    @staticmethod
    def put(id):
        parser = reqparse.RequestParser()
        parser.add_argument('VIP')
        args = parser.parse_args()
        set = Settings().get_glob_settings
        set["VIP"] = args['VIP']
        Settings().set_glob_settings(set)
=======
	@auth.login_required
	def get(self, id):
		set = db.Settings().get_glob_settings()
		return set, 200

	def put(self, id):
		parser = reqparse.RequestParser()
		parser.add_argument('VIP')

		args = parser.parse_args()

		set = db.Settings().get_glob_settings()
		set["VIP"] = args['VIP']

		db.Settings().set_glob_settings(set)

		return set, 201
>>>>>>> lg



class Guild(Resource):
<<<<<<< HEAD
    @auth.login_required
    def get(self, id):

        if not Settings().get_server_settings(str(id)):
            return 'Guild not found', 404
        else:
            set = Settings().get_server_settings(str(id))
            return set, 200

    @staticmethod
    def put(id):
        parser = reqparse.RequestParser()
        parser.add_argument('Greet')
        parser.add_argument('bl')
        parser.add_argument('logging')
        parser.add_argument('GreetChannel')
        parser.add_argument('LogChannel')
        parser.add_argument('Setup')
        parser.add_argument('Mods')
        parser.add_argument('Admins')

        args = parser.parse_args()

        set = Settings().get_user_settings(str(id))
        set["Greet"] = args['Greet']
        set['bl'] = args['bl']
        set['logging'] = args['logging']
        set['GreetChannel'] = args['GreetChannel']
        set['LogChannel'] = args['LogChannel']
        set['Admins'] = args["Admins"]
        set['Mods'] = args['Mods']
        set['Setup'] = args['Setup']
        Settings().set_server_settings(str(id), set)

        return set, 201
=======
	@auth.login_required
	def get(self, id):

		if not db.Settings().get_server_settings(str(id)):
			return 'Guild not found', 404
		else:
			set = db.Settings().get_server_settings(str(id))
			return set, 200

	def put(self, id):
		parser = reqparse.RequestParser()
		parser.add_argument('Greet')
		parser.add_argument('bl')
		parser.add_argument('logging')
		parser.add_argument('GreetChannel')
		parser.add_argument('LogChannel')
		parser.add_argument('automod')
		parser.add_argument('Setup')
		parser.add_argument('Mods')
		parser.add_argument('Admins')

		args = parser.parse_args()

		set = db.Settings().get_user_settings(str(id))
		set["Greet"] = args['Greet']
		set['bl'] = args['bl']
		set['logging'] = args['logging']
		set['GreetChannel'] = args['GreetChannel']
		set['LogChannel'] = args['LogChannel']
		set['automod'] = args['automod']
		set['Admins'] = args["Admins"]
		set['Mods'] = args['Mods']
		set['Setup'] = args['Setup']
		db.Settings().set_server_settings(str(id), set)

		return set, 201

>>>>>>> lg


api.add_resource(Guild, "/guild/<string:id>")
api.add_resource(Global, "/global")

app.run(host='0.0.0.0', port=4437, debug=True)
