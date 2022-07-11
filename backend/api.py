from flask import Flask
from flask_restful import Resource, Api
from Users.UserController import UserController
from Users.UserController import CleanDB

app = Flask(__name__)
api = Api(app)

basePath = '/api/v1'
class TestApi(Resource):
    def get(self):
        return {'message': 'Hi Dad 👋'}, 200

api.add_resource(TestApi, f'{basePath}/')

###### FAKE USERS CONTROLLER #########
api.add_resource(UserController, f'{basePath}/fake-users')
api.add_resource(CleanDB, f'{basePath}/fake-users/clean')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)