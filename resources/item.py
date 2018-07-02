from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',required=True,help="price filed can not be blank")
    parser.add_argument('store_id',required=True,help="Item should have store id!")

    @jwt_required() # require token to get perticulre item
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'Item not found!'}, 404

    def post(self,name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name {} is already exists.".format(name)},400

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])
        try:
            item.save_to_db()  # item is object now
            return {'message':'Item added into database'}, 201
        except:
            return {'message':"An error occurred while inserting data!"}, 500

    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if not item:
            return {'message': "Item not found!"}, 404
        item.delete_from_db()
        return {'message':'Item name {} deleted!'.format(name)}

    def put(self,name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price'] # just updating item price not store id
        else:
            item = ItemModel(name, data['price'], data['store_id'])
        item.save_to_db()
        return item.json(), 201


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
        #return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
