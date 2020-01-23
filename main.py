from os import environ
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Resource, Api
from src.Configuration.Configure import Configuration


def createToken(bot_token):
    from secrets import token_urlsafe
    if environ['BOT_TOKEN'] == bot_token:
        token = token_urlsafe()
        environ['BACKEND_TOKEN'] = token
        return {'token': token}
    else:
        return None


def checkToken(token):
    return token == environ['BACKEND_TOKEN']


app = Flask(__name__)
CORS(app)
api = Api(app)

dbm = Configuration().configure_local_test()


class GetToken(Resource):
    def post(self):
        data = request.get_json()
        token = data['token']
        res = createToken(token)
        return jsonify(res) if res is not None else 500


class AddUser(Resource):
    def post(self):
        data = request.get_json()
        token = data['token']
        username = data['data']['username']
        chat_id = data['data']['chat_id']
        if checkToken(token):
            res = dbm.addUser(chat_id, username)
            return jsonify(res) if res is not None else 500
        else:
            return 403


class AddProduct(Resource):
    def post(self):
        data = request.get_json()
        token = data['token']
        name = data['data']['name']
        price = data['data']['price']
        quantity = data['data']['quantity']
        if checkToken(token):
            res = dbm.addProduct(name, price, quantity)
            return jsonify(res) if res is not None else 500
        else:
            return 403


class EditQuantity(Resource):
    def post(self):
        data = request.get_json()
        token = data['token']
        product_id = data['data']['product_id']
        quantity = data['data']['quantity']
        if checkToken(token):
            res = dbm.editQuantity(product_id, quantity)
            return jsonify(res), 200 if res is not None else 500
        else:
            return 403


class AddTransaction(Resource):
    def post(self):
        data = request.get_json()
        token = data['token']
        chat_id = data['data']['chat_id']
        product_id = data['data']['product_id']
        quantity = data['data']['quantity']
        if checkToken(token):
            res = dbm.addTransaction(chat_id, product_id, quantity)
            return jsonify(res) if res is not None else 500
        else:
            return 403


class GetAllProducts(Resource):
    def post(self):
        data = request.get_json()
        token = data['token']
        if checkToken(token):
            res = dbm.getAllProducts()
            return jsonify(res) if res is not None else 500
        else:
            return 403


class GetAllTransactions(Resource):
    def post(self, token):
        if checkToken(token):
            res = dbm.getAllTransactions()
            return jsonify(res) if res is not None else 500
        else:
            return 403


class GetUserFromUsername(Resource):
    def post(self):
        data = request.get_json()
        token = data['token']
        username = data['data']['username']
        if checkToken(token):
            res = dbm.getUserFromUsername(username)
            return jsonify(res) if res is not None else 500
        else:
            return 403


class GetUserFromChatId(Resource):
    def post(self):
        data = request.get_json()
        token = data['token']
        chat_id = data['data']['chat_id']
        if checkToken(token):
            res = dbm.getUserFromChatId(chat_id)
            return jsonify(res) if res is not None else 500
        else:
            return 403


class GetAllUsers(Resource):
    def post(self):
        data = request.get_json()
        token = data['token']
        if checkToken(token):
            res = dbm.getAllUsers()
            return jsonify(res) if res is not None else 500
        else:
            return 403


class GetAcquistiIn(Resource):
    def post(self, token):
        if checkToken(token):
            return jsonify(dbm.getAcquistiIn())


# TODO: add control to create record if doesn't exists
class ActivateActivator(Resource):
    def post(self, token):
        if checkToken(token):
            return jsonify(dbm.activateActivator())


class DeactivateActivator(Resource):
    def post(self, token):
        if checkToken(token):
            return jsonify(dbm.deactivateActivator())


class CheckActivator(Resource):
    def post(self, token):
        if checkToken(token):
            return jsonify(dbm.checkActivator())


# TODO: add control to create record if doesn't exists
class ActivateBackup(Resource):
    def post(self, token):
        if checkToken(token):
            return jsonify(dbm.activateBackup())


class DeactivateBackup(Resource):
    def post(self, token):
        if checkToken(token):
            return jsonify(dbm.deactivateBackup())


class CheckBackup(Resource):
    def post(self, token):
        if checkToken(token):
            return jsonify(dbm.checkBackup())


api.add_resource(GetToken, '/getToken')
api.add_resource(AddUser, '/addUser')
api.add_resource(AddProduct, '/addProduct')
api.add_resource(EditQuantity, '/editQuantity')
api.add_resource(AddTransaction, '/addTransaction')
api.add_resource(GetAllProducts, '/getAllProducts')
api.add_resource(GetAllTransactions, '/getAllTransactions')
api.add_resource(GetUserFromUsername, '/getUserFromUsername')
api.add_resource(GetUserFromChatId, '/getUserFromChatId')
api.add_resource(GetAllUsers, '/getAllUsers')
api.add_resource(GetAcquistiIn, '/getAcquistiIn')
api.add_resource(ActivateActivator, '/activateActivator')
api.add_resource(DeactivateActivator, '/deactivateActivator')
api.add_resource(CheckActivator, '/checkActivator')
api.add_resource(ActivateBackup, '/activateBackup')
api.add_resource(DeactivateBackup, '/deactivateBackup')
api.add_resource(CheckBackup, '/checkBackup')



if __name__ == '__main__':
    app.run(debug=True)