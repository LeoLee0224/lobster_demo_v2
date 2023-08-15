from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import asyncio
import time
        
class TimeSet(Resource):
    time = 3
    def get(self):
        TimeSet.time = self.call_time()
        return "finished"
    
    def call_time(self):
        time.sleep(2)
        return 10


class HelloWorld(Resource):
    def get(self):
        return "helloworld!!!"

class sever:
    def __init__(self) -> None:
        pass
    def run(self):
        app = Flask(__name__)
        api = Api(app)
        api.add_resource(TimeSet, '/timeset')
        api.add_resource(HelloWorld,'/')
        app.run()

