import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', help="This field cannot be blank!", required=True)
    parser.add_argument('password', help="This field cannot be blank!", required=True)

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': "User already exists in database!"}, 400

        user = UserModel(**data)
        user.save_to_db()
        return {'message':"User created successfully."}, 201
