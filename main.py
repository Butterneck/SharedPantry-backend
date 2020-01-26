from os import environ
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Resource, Api
from src.Configuration.Configure import Configuration
from dateutil.parser import parse
import logging


def createToken(bot_token):
    from secrets import token_urlsafe
    if environ['BOT_TOKEN'] == bot_token:
        token = token_urlsafe()
        environ['BACKEND_TOKEN'] = token
        logging.debug(environ['BACKEND_TOKEN'])
        return {'token': token}
    else:
        return None


def checkToken(request):
    return request.headers.get('token') == environ['BACKEND_TOKEN']


app = Flask(__name__)
CORS(app)
api = Api(app)

dbm = Configuration().configure()


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
    def post(self):
        if checkToken(request):
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
        else:
            response = jsonify(None)
            response.status_code = 403

        return response


class AddProduct(Resource):
    def post(self):
        if checkToken(request):
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
        else:
            response = jsonify(None)
            response.status_code = 403

        return response


class EditProductQuantity(Resource):
    def post(self):
        if checkToken(request):
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
        else:
            response = jsonify(None)
            response.status_code = 403

        return response


class EditProductName(Resource):
    def post(self):
        if checkToken(request):
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
        else:
            response = jsonify(None)
            response.status_code = 403

        return response


class EditProductPrice(Resource):
    def post(self):
        if checkToken(request):
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
        else:
            response = jsonify(None)
            response.status_code = 403

        return response


class AddTransaction(Resource):
    def post(self):
        if checkToken(request):
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
        else:
            response = jsonify(None)
            response.status_code = 403

        return response


class GetAllProducts(Resource):
    def post(self):
        if checkToken(request):
            res = dbm.getAllProducts()
            if res is not None:
                response = jsonify(res)
                response.status_code = 200
            else:
                response = jsonify(None)
                response.status_code = 500
        else:
            response = jsonify(None)
            response.status_code = 403

        return response


class GetAllTransactions(Resource):
    def post(self):
        if checkToken(request):
            res = dbm.getAllTransactions()
            if res is not None:
                response = jsonify(res)
                response.status_code = 200
            else:
                response = jsonify(None)
                response.status_code = 500
        else:
            response = jsonify(None)
            response.status_code = 403

        return response


class GetUserFromUsername(Resource):
    def post(self):
        if checkToken(request):
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
        else:
            response = jsonify(None)
            response.status_code = 403

        return response


class GetUserFromChatId(Resource):
    def post(self):
        if checkToken(request):
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
        else:
            response = jsonify(None)
            response.status_code = 403

        return response


class GetAllUsers(Resource):
    def post(self):
        if checkToken(request):
            res = dbm.getAllUsers()
            if res is not None:
                response = jsonify(res)
                response.status_code = 200
            else:
                response = jsonify(None)
                response.status_code = 500
        else:
            response = jsonify(None)
            response.status_code = 403

        return response


class GetAllAdmins(Resource):
    def post(self):
        if checkToken(request):
            res = dbm.getAllAdmins()
            if res is not None:
                response = jsonify(res)
                response.status_code = 200
            else:
                response = jsonify(None)
                response.status_code = 500
        else:
            response = jsonify(None)
            response.status_code = 403

        return response


class EditUserAdmin(Resource):
    def post(self):
        if checkToken(request):
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
        else:
            response = jsonify(None)
            response.status_code = 403

        return response


class EditUserName(Resource):
    def post(self):
        if checkToken(request):
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
        else:
            response = jsonify(None)
            response.status_code = 403

        return response


class GetAcquistiIn(Resource):
    def post(self):
        if checkToken(request):
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
        else:
            response = jsonify(None)
            response.status_code = 403

        return response


class Backup(Resource):
    def post(self):
        if checkToken(request):
            res = dbm.backup()
            response = jsonify(None)
            if res is not None:
                response.status_code = 200
            else:
                response.status_code = 500
        else:
            response = jsonify(None)
            response.status_code = 403

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