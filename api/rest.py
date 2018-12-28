from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from flask_httpauth import HTTPBasicAuth


from db import Settings

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    set = Settings().get_key_settings(str(username))
    if not set:
        return None
    else:
        return set[str('key')]


@auth.error_handler
def unauthorized():
    return 'Not authorized', 404

class Global(Resource):
    @auth.login_required
    

    def get(self, id):
            set = Settings().get_glob_settings()
            return set, 200

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('VIP')


        args = parser.parse_args()

        set = Settings().get_glob_settings()
        set["VIP"] = args['VIP']

        Settings().set_glob_settings(set)

        return set, 201

class Guild(Resource):
    @auth.login_required
    def get(self, id):

        if not Settings().get_server_settings(str(id)):
            return 'Guild not found', 404
        else:
            set = Settings().get_server_settings(str(id))
            return set, 200

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('Greet')
        parser.add_argument('bl')
        parser.add_argument('logging')
        parser.add_argument('GreetChannel')
        parser.add_argument('LogChannel')
        parser.add_argument('automod')


        args = parser.parse_args()

        set = Settings().get_user_settings(str(id))
        set["Greet"] = args['Greet']
        set['bl'] = args['bl']
        set['logging'] = args['logging']
        set['GreetChannel'] = args['GreetChannel']
        set['automod'] = args['automod']

        Settings().set_server_settings(str(id), set)

        return set, 201


class User(Resource):
    @auth.login_required
    def get(self, id):

        if not Settings().get_user_settings(str(id)):
            return "User not found", 404
        else:
            set = Settings().get_user_settings(str(id))
            return set, 200

    def post(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('gender')
        parser.add_argument('status')
        parser.add_argument('lover')
        parser.add_argument('desc')
        args = parser.parse_args()

        if Settings().get_user_settings(str(id)):
            return "User already exist", 404
        else:
            set = Settings().get_user_settings(str(id))
            set["gender"] = args['gender']
            set['status'] = args['status']
            set['lover'] = args['lover']
            set['desc'] = args['desc']

            Settings().set_user_settings(str(id), set)

        return set, 201

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('gender')
        parser.add_argument('status')
        parser.add_argument('lover')
        parser.add_argument('desc')

        args = parser.parse_args()

        set = Settings().get_user_settings(str(id))
        set["gender"] = args['gender']
        set['status'] = args['status']
        set['lover'] = args['lover']
        set['desc'] = args['desc']

        Settings().set_user_settings(str(id), set)

        return set, 201


api.add_resource(User, "/user/<string:id>")

app.run(host='0.0.0.0', port=4437, debug=True)
