from main import db
import logging

from src.DBClasses.User import User as User
from src.DBClasses.Product import Product
from src.DBClasses.Transaction import Transaction
from src.DBClasses.Debit import Debit


def addUser(chat_id, username, lang, is_admin):
    from src.DBClasses.User import User as User
    user = User(chat_id, username, lang, is_admin)
    db.session.add(user)
    db.session.commit()
    return {'user': {
        'id': user.chat_id,
        'username': user.username,
        'lang': user.lang,
        'isAdmin': is_admin
        }
    }

def addProduct(name, price, qt):
    from src.DBClasses.Product import Product
    product = Product(name, price, qt)
    db.session.add(product)
    db.session.commit()
    return {'product': {
        'id': product.id,
        'name': product.name,
        'quantity': product.quantity,
        'price': product.price
        }
    }

def editProductQuantity(product_id, qt):
    from src.DBClasses.Product import Product
    product = Product.query.filter_by(id=product_id).first()
    product.quantity = qt
    db.session.commit()

    return {'product': {
        'id': product.id,
        'name': product.name,
        'quantity': product.quantity,
        'price': product.price
        }
    } if product is not None else None

def editProductName(product_id, name):
    from src.DBClasses.Product import Product
    product = Product.query.filter_by(id=product_id).first()
    product.name = name
    db.session.commit()
    return {'product': {
        'id': product.id,
        'name': product.name,
        'quantity': product.quantity,
        'price': product.price
        }
    } if product is not None else None

def editProductPrice(product_id, price):
    from src.DBClasses.Product import Product
    product = Product.query.filter_by(id=product_id).first()
    product.price = price
    db.session.commit()
    return {'product': {
        'id': product.id,
        'name': product.name,
        'quantity': product.quantity,
        'price': product.price
        }
    } if product is not None else None

def addTransaction(chat_id, product_id, qt):
    from src.DBClasses.Transaction import Transaction
    from datetime import datetime
    if not checkAvailability(product_id):
        return None
    pick_up(product_id)
    transaction = Transaction(chat_id, product_id, datetime.now().replace(microsecond=0), qt)
    db.session.add(transaction)
    db.session.commit()
    return {'transaction': {
        'user_id': transaction.user_id,
        'product_id': transaction.product_id,
        'date': transaction.date,
        'quantity': transaction.quantity
        }
    }

def checkAvailability(product_id):
    from src.DBClasses.Product import Product
    quantity = Product.query.filter_by(id=product_id).first().quantity
    return quantity

def pick_up(product_id):
    from src.DBClasses.Product import Product
    current_quantity = Product.query.filter_by(id=product_id).first().quantity
    editProductQuantity(product_id, current_quantity - 1)

def getAllProducts():
    from src.DBClasses.Product import Product
    products = []
    for product in Product.query.all():
        products.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'quantity': product.quantity
        })
    return {'products': products} if products is not None else None

def getAllTransactions():
    from src.DBClasses.Transaction import Transaction
    transactions = []
    for transaction in Transaction.query.all():
        transactions.append({
            'user_id': transaction.user_id,
            'product_id': transaction.product_id,
            'date': transaction.date,
            'quantity': transaction.quantity
        })

    return {'transactions': transactions} if transactions is not None else None

def getAllTransactionsFrequency():
    from src.DBClasses.Transaction import Transaction
    transactions = getAllTransactions()['transactions']
    if transactions is None: return None
    count = countTransactions(transactions)
    return {'frequencies': count} if count is not None else None

def countTransactions(transactions):
    from src.DBClasses.Product import Product
    products = getAllProducts()['products']
    if products is None: return None
    frequency = {}
    for transaction in transactions:
        product_name = getProductNameFromId(products, transaction['product_id'])
        if product_name is None: return None
        try:
            frequency[product_name] += 1
        except KeyError:
            frequency[product_name] = 1
    return frequency

def getProductNameFromId(products, id):
    for product in products:
        if product['id'] == id:
            return product['name']
    return None

def getUserFromUsername(username):
    from src.DBClasses.User import User
    user = User.query.filter_by(username=username).first()
    return {'user': {
            'chat_id': user.chat_id,
            'username': user.username,
            'lang': user.lang,
            'is_admin': user.is_admin
        }
    } if user is not None else None

def getUserFromChatId(chat_id):
    from src.DBClasses.User import User
    user = User.query.filter_by(chat_id=chat_id).first()
    if user is not None:
        return {'user': {
                'chat_id': user.chat_id,
                'username': user.username,
                'lang': user.lang,
                'is_admin': user.is_admin
            }
        }
    else:
        return None

def getAllUsers():
    from src.DBClasses.User import User
    users = []
    for user in User.query.all():
        users.append({
            'chat_id': user.chat_id,
            'username': user.username,
            'lang': user.lang,
            'is_admin': user.is_admin
        })
    return {'users': users} if users is not None else None

def getAllAdmins():
    from src.DBClasses.User import User
    admins = []
    for admin in User.query.filter_by(is_admin=True):
        admins.append({
            'chat_id': admin.chat_id,
            'username': admin.username,
            'lang': admin.lang,
            'is_admin': admin.is_admin
        })
    return {'admins': admins} if admins is not None else None

def editUserName(caht_id, username):
    from src.DBClasses.User import User
    user = User.query.filter_by(chat_id=caht_id).first()
    user.username = username
    db.session.commit()
    return {'user': {
        'chat_id': user.chat_id,
        'username': user.username,
        'lang': user.lang,
        'is_admin': user.is_admin
        }
    } if user is not None else None

def editUserAdmin(chat_id, is_admin):
    from src.DBClasses.User import User
    user = User.query.filter_by(chat_id=chat_id).first()
    db.session.commit()
    return {'user': {
        'chat_id': user.chat_id,
        'username': user.username,
        'lang': user.lang,
        'is_admin': is_admin
        }
    } if user is not None else None

def editUserLang(chat_id, lang):
    from src.DBClasses.User import User
    user = User.query.filter_by(chat_id=chat_id).first()
    user.lang = lang
    db.session.commit()
    return {'user': {
        'chat_id': user.chat_id,
        'username': user.username,
        'lang': user.lang,
        'is_admin': user.is_admin
        }
    } if user is not None else None

def getAcquistiIn(user_id, startDate, endDate):
    from src.DBClasses.Transaction import Transaction
    transactions = []
    for transaction in Transaction.query.filter_by(user_id=user_id).filter(Transaction.date >= startDate).filter(Transaction.date <= endDate).all():
        transactions.append({
            'user_id': transaction.user_id,
            'product_id': transaction.product_id,
            'date': str(transaction.date),
            'quantity': str(transaction.quantity)
        })
    return {'transactions': transactions} if transactions is not None else None
