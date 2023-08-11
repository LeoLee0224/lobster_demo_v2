from flask import Flask, request, jsonify
from flask_restful import Api, Resource

user_list = []
class User(Resource):
    def get(self, username):
        for user in user_list:
            if user['username'] == username:
                return user
        return {'username': None}, 404
    def post(self, username):
        user = {
            'username': username,
            'email': request.get_json().get('email')
        }
        user_list.append(user)
        return user
    def delete(self, username):
        for ind, user in enumerate(user_list):
            if user['username'] == username:
                deleted_user = user_list.pop(ind)
                print(deleted_user)
                return {'note': 'successfully delete'}
    def put(self, username):
        user_find = None
        for user in user_list:
            if user['username'] == username:
                user_find = user
        if user_find:
            user_list.remove(user_find)
            user_find['email'] = request.get_json().get('email')
            user_list.append(user_find)
            return user_find
        
class UserList(Resource):
    """會員列表 """
    def get(self):
        return {'user_list': user_list}
    
class HelloWorld(Resource):
    def get(self):
        return "helloworld!!!"

class sever:
    def __init__(self) -> None:
        pass
    def run(self):
        app = Flask(__name__)
        api = Api(app)
        api.add_resource(User, '/user/<string:username>')
        api.add_resource(UserList, '/users')
        api.add_resource(HelloWorld,'/')
        app.run()

