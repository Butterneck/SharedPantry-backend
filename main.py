from os import environ
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Resource, Api
from src.Configuration.Configure import Configuration
from dateutil.parser import parse
import jwt
from functools import wraps
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
CORS(app)
api = Api(app)

app.config['BOT_TOKEN'] = environ['BOT_TOKEN']
app.config['SECRET_KEY'] = environ['SECRET_KEY']


app.config['SQLALCHEMY_DATABASE_URI'] = Configuration().configure()
db = SQLAlchemy(app)

import src.db_manager as dbm


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('token')

        if not token:
            response = jsonify(None)
            response.status_code = 403
            return response
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            response = jsonify(None)
            response.status_code = 403
            return response
        return f(*args, **kwargs)
    return decorated


def createToken(bot_token):
    if app.config['BOT_TOKEN'] == bot_token:
        from secrets import token_urlsafe
        token = jwt.encode({'token': token_urlsafe()}, app.config['SECRET_KEY'])
        return {'token': token.decode('UTF-8')}
    else:
        return None


class GetToken(Resource):
    def post(self):
        res = createToken(request.headers.get('token'))
        if res is not None:
            response = jsonify(res)
            response.status_code = 200
        else:
            response = jsonify(None)
            response.status_code = 403
        return response


class AddUser(Resource):
    @token_required
    def post(self):
        data = request.get_json()
        try:
            username = data['username']
            chat_id = data['chat_id']
            lang = data['lang']
        except KeyError:
            response = jsonify(None)
            response.status_code = 400
            return response
        res = dbm.addUser(chat_id, username, lang)
        if res is not None:
            response = jsonify(res)
            response.status_code = 200
        else:
            response = jsonify(None)
            response.status_code = 500

        return response


class AddProduct(Resource):
    @token_required
    def post(self):
        data = request.get_json()
        try:
            name = data['name']
            price = data['price']
            quantity = data['quantity']
        except KeyError:
            response = jsonify(None)
            response.status_code = 400
            return response
        res = dbm.addProduct(name, price, quantity)
        if res is not None:
            response = jsonify(res)
            response.status_code = 200
        else:
            response = jsonify(None)
            response.status_code = 500

        return response


class EditProductQuantity(Resource):
    @token_required
    def post(self):
        data = request.get_json()
        try:
            product_id = data['product_id']
            quantity = data['quantity']
        except KeyError:
            response = jsonify(None)
            response.status_code = 400
            return response
        res = dbm.editProductQuantity(product_id, quantity)
        if res is not None:
            response = jsonify(res)
            response.status_code = 200
        else:
            response = jsonify(None)
            response.status_code = 500

        return response


class EditProductName(Resource):
    @token_required
    def post(self):
        data = request.get_json()
        try:
            product_id = data['product_id']
            name = data['name']
        except KeyError:
            response = jsonify(None)
            response.status_code = 400
            return response
        res = dbm.editProductName(product_id, name)
        if res is not None:
            response = jsonify(res)
            response.status_code = 200
        else:
            response = jsonify(None)
            response.status_code = 500

        return response


class EditProductPrice(Resource):
    @token_required
    def post(self):
        data = request.get_json()
        try:
            product_id = data['product_id']
            price = data['price']
        except KeyError:
            response = jsonify(None)
            response.status_code = 400
            return response
        res = dbm.editProductPrice(product_id, price)
        if res is not None:
            response = jsonify(res)
            response.status_code = 200
        else:
            response = jsonify(None)
            response.status_code = 500

        return response


class AddTransaction(Resource):
    @token_required
    def post(self):
        data = request.get_json()
        try:
            chat_id = data['chat_id']
            product_id = data['product_id']
            quantity = data['quantity']
        except KeyError:
            response = jsonify(None)
            response.status_code = 400
            return response
        res = dbm.addTransaction(chat_id, product_id, quantity)
        if res is not None:
            response = jsonify(res)
            response.status_code = 200
        else:
            response = jsonify(None)
            response.status_code = 500

        return response


class GetAllProducts(Resource):
    @token_required
    def post(self):
        res = dbm.getAllProducts()
        if res is not None:
            response = jsonify(res)
            response.status_code = 200
        else:
            response = jsonify(None)
            response.status_code = 500

        return response


class GetAllTransactions(Resource):
    @token_required
    def post(self):
        res = dbm.getAllTransactions()
        if res is not None:
            response = jsonify(res)
            response.status_code = 200
        else:
            response = jsonify(None)
            response.status_code = 500

        return response


class GetUserFromUsername(Resource):
    @token_required
    def post(self):
        data = request.get_json()
        try:
            username = data['username']
        except KeyError:
            response = jsonify(None)
            response.status_code = 400
            return response
        res = dbm.getUserFromUsername(username)
        if res is not None:
            response = jsonify(res)
            response.status_code = 200
        else:
            response = jsonify(None)
            response.status_code = 500

        return response


class GetUserFromChatId(Resource):
    @token_required
    def post(self):
        data = request.get_json()
        try:
            chat_id = data['chat_id']
        except KeyError:
            response = jsonify(None)
            response.status_code = 400
            return response
        res = dbm.getUserFromChatId(chat_id)
        if res is not None:
            response = jsonify(res)
            response.status_code = 200
        else:
            response = jsonify(None)
            response.status_code = 500

        return response


class GetAllUsers(Resource):
    @token_required
    def post(self):
        res = dbm.getAllUsers()
        if res is not None:
            response = jsonify(res)
            response.status_code = 200
        else:
            response = jsonify(None)
            response.status_code = 500

        return response


class GetAllAdmins(Resource):
    @token_required
    def post(self):
        res = dbm.getAllAdmins()
        if res is not None:
            response = jsonify(res)
            response.status_code = 200
        else:
            response = jsonify(None)
            response.status_code = 500

        return response


class EditUserAdmin(Resource):
    @token_required
    def post(self):
        data = request.get_json()
        try:
            chat_id = data['chat_id']
        except KeyError:
            response = jsonify(None)
            response.status_code = 400
            return response
        res = dbm.editUserAdmin(chat_id)
        if res is not None:
            response = jsonify(res)
            response.status_code = 200
        else:
            response = jsonify(None)
            response.status_code = 500

        return response


class UpdateUserLang(Resource):
    @token_required
    def post(self):
        data = request.get_json()
        try:
            chat_id = data['chat_id']
            lang = data['lang']
        except KeyError:
            response = jsonify(None)
            response.status_code = 400
            return response
        res = dbm.editUserLang(chat_id, lang)
        if res is not None:
            response = jsonify(res)
            response.status_code = 200
        else:
            response = jsonify(None)
            response.status_code = 500

        return response


class EditUserName(Resource):
    @token_required
    def post(self):
        data = request.get_json()
        try:
            chat_id = data['chat_id']
            username = data['username']
        except KeyError:
            response = jsonify(None)
            response.status_code = 400
            return response
        res = dbm.editUserName(chat_id, username)
        if res is not None:
            response = jsonify(res)
            response.status_code = 200
        else:
            response = jsonify(None)
            response.status_code = 500

        return response


class GetAcquistiIn(Resource):
    @token_required
    def post(self):
        data = request.get_json()
        try:
            user_id = data['user_id']
            start_date = parse(data['start_date'])
            end_date = parse(data['end_date'])
        except KeyError:
            response = jsonify(None)
            response.status_code = 400
            return response
        res = dbm.getAcquistiIn(user_id, start_date, end_date)
        if res is not None:
            response = jsonify(res)
            response.status_code = 200
        else:
            response = jsonify(None)
            response.status_code = 500

        return response


class Backup(Resource):
    @token_required
    def post(self):
        res = dbm.backup()
        response = jsonify(None)
        if res is not None:
            response.status_code = 200
        else:
            response.status_code = 500

        return response


api.add_resource(GetToken, '/api/getToken')
api.add_resource(AddUser, '/api/addUser')
api.add_resource(AddProduct, '/api/addProduct')
api.add_resource(EditProductQuantity, '/api/editProductQuantity')
api.add_resource(EditProductName, '/api/editProductName')
api.add_resource(EditProductPrice, '/api/editProductPrice')
api.add_resource(EditUserName, '/api/editUserName')
api.add_resource(EditUserAdmin, '/api/editUserAdmin')
api.add_resource(AddTransaction, '/api/addTransaction')
api.add_resource(GetAllProducts, '/api/getAllProducts')
api.add_resource(GetAllTransactions, '/api/getAllTransactions')
api.add_resource(GetUserFromUsername, '/api/getUserFromUsername')
api.add_resource(GetUserFromChatId, '/api/getUserFromChatId')
api.add_resource(GetAllUsers, '/api/getAllUsers')
api.add_resource(GetAllAdmins, '/api/getAllAdmins')
api.add_resource(GetAcquistiIn, '/api/getAcquistiIn')
api.add_resource(UpdateUserLang, '/api/updateUserLang')
api.add_resource(Backup, '/api/backup')


from src.DBClasses.User import User
from src.DBClasses.Product import Product
from src.DBClasses.Transaction import Transaction
db.create_all()
db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)