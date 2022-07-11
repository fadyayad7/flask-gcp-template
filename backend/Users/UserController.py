from flask import request
from flask_restful import Resource
from Users.UserManager import UserManager
from .SchemaValidator import PostUserSchema

userManager = UserManager()

class UserController(Resource):
    def get(self):
        return userManager.get(), 200
    
    def post(self):
        body = request.json
        try:
            PostUserSchema().load(body)
        except Exception as e:
            return None, 400
        return userManager.post(body['username']), 200

class CleanDB(Resource):
    def get(self):
        userManager._clean()

    

