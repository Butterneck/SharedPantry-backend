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
        if res is not None:
            response = jsonify(res)
            response.status_code = 200
        else:
            response = jsonify(None)
            response.status_code = 403
        return response


class AddUser(Resource):
    def post(self):
        data = request.get_json()
        token = data['token']
        username = data['data']['username']
        chat_id = data['data']['chat_id']
        if checkToken(token):
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
        data = request.get_json()
        token = data['token']
        name = data['data']['name']
        price = data['data']['price']
        quantity = data['data']['quantity']
        if checkToken(token):
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


class EditQuantity(Resource):
    def post(self):
        data = request.get_json()
        token = data['token']
        product_id = data['data']['product_id']
        quantity = data['data']['quantity']
        if checkToken(token):
            res = dbm.editQuantity(product_id, quantity)
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
        data = request.get_json()
        token = data['token']
        chat_id = data['data']['chat_id']
        product_id = data['data']['product_id']
        quantity = data['data']['quantity']
        if checkToken(token):
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
        data = request.get_json()
        token = data['token']
        if checkToken(token):
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
    def post(self, token):
        if checkToken(token):
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
        data = request.get_json()
        token = data['token']
        username = data['data']['username']
        if checkToken(token):
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
        data = request.get_json()
        token = data['token']
        chat_id = data['data']['chat_id']
        if checkToken(token):
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
        data = request.get_json()
        token = data['token']
        if checkToken(token):
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


class GetAcquistiIn(Resource):
    def post(self, token):
        data = request.get_json()
        token = data['token']
        user_id = data['data']['user_id']
        start_date = data['data']['start_date']
        end_date = data['data']['end_date']
        if checkToken(token):
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