from flask import Flask
from flask_restful import Resource, Api
from utils import Connector

app = Flask(__name__)
api = Api(app)

basePath = '/api/v1'

#connector = Connector()

# class VisitCounter(Resource):
#     def patch(self, page):
#         if len(page) <= 2:
#             return None, 400
#         connector.update_counter(page)
#         return None, 200

# api.add_resource(VisitCounter, f'{basePath}/visits/<string:page>')

class TestApi(Resource):
    def get(self):
        return {'message': 'Hi Dad 👋'}, 200

api.add_resource(TestApi, f'{basePath}/')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)