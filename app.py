# create item based on name using post method, get specific item or list of items using get method, update item using put and delete item using del method.

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT, timedelta

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item,ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # turn off flask SQLAlchemy modification.
app.secret_key = 'key123'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Store,'/store/<string:name>')
api.add_resource(Item,'/item/<string:name>') # http://localhost:5000/student/Rolf
api.add_resource(ItemList,'/items')
api.add_resource(StoreList,'/stores')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)
