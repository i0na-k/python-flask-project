from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from app_code.security import authenticate, identity

app = Flask(__name__)
api = Api(app)

app.secret_key = 'pa$$word'

jwt = JWT(app, authenticate, identity)
items = []


class Item(Resource):
    @jwt_required()
    def get(self, name):

        item = next(filter(lambda item: item['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda item: item['name'] == name,items), None) is not None:
            return {'message': "An item with name '{}' already exists".format(name)},400

        data = request.get_json()
        item = {'name': name,
                'price': data['price']
                }
        items.append(item)
        return item, 201


class ItemList(Resource):
    def get(self):
        return {'items': items}, 200


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)