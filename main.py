from os import environ
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Resource, Api
from src.Configuration.Configure import Configuration
from dateutil.parser import parse
import jwt
from functools import wraps


app = Flask(__name__)
CORS(app)
api = Api(app)

app.config['BOT_TOKEN'] = environ['BOT_TOKEN']
app.config['SECRET_KEY'] = environ['SECRET_KEY']


dbm = Configuration().configure()


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
        except KeyError:
            response = jsonify(None)
            response.status_code = 400
            return response
        res = dbm.addUser(chat_id, username)
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


api.add_resource(GetToken, '/getToken')
api.add_resource(AddUser, '/addUser')
api.add_resource(AddProduct, '/addProduct')
api.add_resource(EditProductQuantity, '/editProductQuantity')
api.add_resource(EditProductName, '/editProductName')
api.add_resource(EditProductPrice, '/editProductPrice')
api.add_resource(EditUserName, '/editUserName')
api.add_resource(EditUserAdmin, '/editUserAdmin')
api.add_resource(AddTransaction, '/addTransaction')
api.add_resource(GetAllProducts, '/getAllProducts')
api.add_resource(GetAllTransactions, '/getAllTransactions')
api.add_resource(GetUserFromUsername, '/getUserFromUsername')
api.add_resource(GetUserFromChatId, '/getUserFromChatId')
api.add_resource(GetAllUsers, '/getAllUsers')
api.add_resource(GetAllAdmins, '/getAllAdmins')
api.add_resource(GetAcquistiIn, '/getAcquistiIn')
api.add_resource(Backup, '/backup')



if __name__ == '__main__':
    app.run(debug=True)