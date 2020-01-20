from os import environ
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from src.db_manager import DB_Manager


def createToken(bot_token):
    from secrets import token_urlsafe
    if environ['BOT_TOKEN'] == bot_token:
        token = token_urlsafe()
        environ['BACKEND_TOKEN'] = token
        return {'token': token}


def checkToken(token):
    return token == environ['BACKEND_TOKEN']


app = Flask(__name__)
api = Api(app)

dbm = DB_Manager('')


class GetToken(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        token = data['token']
        return jsonify(createToken(token))


class AddUser(Resource):
    def post(self):
        data = request.get_json()
        token = data['token']
        username = data['data']['username']
        chat_id = data['data']['chat_id']
        if checkToken(token):
            return jsonify(dbm.addUser(chat_id, username))


class AddProduct(Resource):
    def post(self):
        data = request.get_json()
        token = data['token']
        name = data['data']['name']
        price = data['data']['price']
        quantity = data['data']['quantity']
        if checkToken(token):
            return jsonify(dbm.addProduct(name, price, quantity))


class EditQuantity(Resource):
    def post(self):
        data = request.get_json()
        token = data['token']
        product_id = data['data']['product_id']
        quantity = data['data']['quantity']
        if checkToken(token):
            return jsonify(dbm.editQuantity(product_id, quantity))


class AddTransaction(Resource):
    def post(self):
        data = request.get_json()
        token = data['token']
        chat_id = data['data']['chat_id']
        product_id = data['data']['product_id']
        quantity = data['data']['quantity']
        if checkToken(token):
            return jsonify(dbm.addTransaction(chat_id, product_id, quantity))


class GetAllProducts(Resource):
    def post(self):
        data = request.get_json()
        token = data['token']
        if checkToken(token):
            return jsonify(dbm.getAllProducts())


class GetAllTransactions(Resource):
    def post(self, token):
        if checkToken(token):
            return jsonify(dbm.getAllTransactions())


class GetUserFromUsername(Resource):
    def post(self):
        data = request.get_json()
        token = data['token']
        username = data['data']['username']
        if checkToken(token):
            return jsonify(dbm.getUserFromUsername(username))


class GetUserFromChatId(Resource):
    def post(self):
        data = request.get_json()
        token = data['token']
        chat_id = data['data']['chat_id']
        if checkToken(token):
            return jsonify(dbm.getUserFromUsername(chat_id))


class GetAllUsers(Resource):
    def post(self):
        data = request.get_json()
        token = data['token']
        if checkToken(token):
            return jsonify(dbm.getAllUsers())


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