from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import logging

Base = declarative_base()


class DB_Manager():

    def __init__(self, db_url):
        self.engine = create_engine(db_url)

        # Need to import those classes after Base declaration to avoid importing errors
        from src.DBClasses.User import User as User
        from src.DBClasses.Product import Product
        from src.DBClasses.Transaction import Transaction
        from src.DBClasses.Debit import Debit

        # Creating schema
        Base.metadata.create_all(self.engine)

        # Creating session
        self.Session = sessionmaker(bind=self.engine)

    def addUser(self, chat_id, username):
        from src.DBClasses.User import User as User
        user = User(chat_id, username)
        session = self.Session()
        session.add(user)
        session.commit()
        return {'user': {
            'id': user.chat_id,
            'username': user.username
            }
        }

    def addProduct(self, name, price, qt):
        from src.DBClasses.Product import Product
        product = Product(name, price, qt)
        session = self.Session()
        session.add(product)
        session.commit()
        return {'product': {
            'id': product.id,
            'name': product.name,
            'quantity': product.quantity,
            'price': product.price
            }
        }

    def editProductQuantity(self, product_id, qt):
        from src.DBClasses.Product import Product
        session = self.Session()
        product = session.query(Product).filter_by(id=product_id).first()
        product.quantity = qt
        session.commit()
        return {'product': {
            'id': product.id,
            'name': product.name,
            'quantity': product.quantity,
            'price': product.price
            }
        } if product is not None else None

    def editProductName(self, product_id, name):
        from src.DBClasses.Product import Product
        session = self.Session()
        product = session.query(Product).filter_by(id=product_id).first()
        product.name = name
        session.commit()
        return {'product': {
            'id': product.id,
            'name': product.name,
            'quantity': product.quantity,
            'price': product.price
            }
        } if product is not None else None

    def editProductPrice(self, product_id, price):
        from src.DBClasses.Product import Product
        session = self.Session()
        product = session.query(Product).filter_by(id=product_id).first()
        product.price = price
        session.commit()
        return {'product': {
            'id': product.id,
            'name': product.name,
            'quantity': product.quantity,
            'price': product.price
            }
        } if product is not None else None

    def addTransaction(self, chat_id, product_id, qt):
        from src.DBClasses.Transaction import Transaction
        from datetime import datetime
        if not self.checkAvailability(product_id):
            return None
        self.pick_up(product_id)
        transaction = Transaction(chat_id, product_id, datetime.now().replace(microsecond=0), qt)
        session = self.Session()
        session.add(transaction)
        session.commit()
        return {'transaction': {
            'user_id': transaction.user_id,
            'product_id': transaction.product_id,
            'date': transaction.date,
            'quantity': transaction.quantity
            }
        }

    def checkAvailability(self, product_id):
        from src.DBClasses.Product import Product
        session = self.Session()
        return session.query(Product).filter_by(id=product_id).first().quantity

    def pick_up(self, product_id):
        from src.DBClasses.Product import Product
        session = self.Session()
        current_quantity = session.query(Product).filter_by(id=product_id).first().quantity
        self.editProductQuantity(product_id, current_quantity - 1)

    def getAllProducts(self):
        from src.DBClasses.Product import Product
        session = self.Session()
        products = []
        for product in session.query(Product).all():
            products.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'quantity': product.quantity
            })
        return {'products': products} if products is not None else None

    def getAllTransactions(self):
        from src.DBClasses.Transaction import Transaction
        session = self.Session()
        transactions = []
        for transaction in session.query(Transaction).all():
            transactions.append({
                'user_id': transaction.user_id,
                'product_id': transaction.product_id,
                'date': transaction.date,
                'quantity': transaction.quantity
            })
        return {'transactions': transactions} if transactions is not None else None

    def getUserFromUsername(self, username):
        from src.DBClasses.User import User
        session = self.Session()
        user = session.query(User).filter_by(username=username).first()
        return {'user': {
                'chat_id': user.chat_id,
                'username': user.username,
                'is_admin': user.is_admin
            }
        } if user is not None else None

    def getUserFromChatId(self, chat_id):
        from src.DBClasses.User import User
        session = self.Session()
        user = session.query(User).filter_by(chat_id=chat_id).first()
        if user is not None:
            return {'user': {
                    'chat_id': user.chat_id,
                    'username': user.username,
                    'is_admin': user.is_admin
                }
            }
        else:
            return None

    def getAllUsers(self):
        from src.DBClasses.User import User
        session = self.Session()
        users = []
        for user in session.query(User).all():
            users.append({
                'chat_id': user.chat_id,
                'username': user.username,
                'is_admin': user.is_admin
            })
        return {'users': users} if users is not None else None

    def getAllAdmins(self):
        from src.DBClasses.User import User
        session = self.Session()
        admins = []
        for admin in session.query(User).filter_by(is_admin=True):
            admins.append({
                'chat_id': admin.chat_id,
                'username': admin.username,
                'is_admin': admin.is_admin
            })
        return {'admins': admins} if admins is not None else None

    def editUserName(self, caht_id, username):
        from src.DBClasses.User import User
        session = self.Session()
        user = session.query(User).filter_by(chat_id=caht_id).first()
        user.username = username
        session.commit()
        return {'user': {
            'chat_id': user.chat_id,
            'username': user.username,
            'is_admin': user.is_admin
            }
        } if user is not None else None

    def editUserAdmin(self, chat_id):
        from src.DBClasses.User import User
        session = self.Session()
        user = session.query(User).filter_by(chat_id=chat_id).first()
        user.is_admin = not user.is_admin
        session.commit()
        return {'user': {
            'chat_id': user.chat_id,
            'username': user.username,
            'is_admin': user.is_admin
            }
        } if user is not None else None

    def getAcquistiIn(self, user_id, startDate, endDate):
        from src.DBClasses.Transaction import Transaction
        session = self.Session()
        transactions = []
        for transaction in session.query(Transaction).filter_by(user_id=user_id).filter(Transaction.date >= startDate).filter(Transaction.date <= endDate).all():
            transactions.append({
                'user_id': transaction.user_id,
                'product_id': transaction.product_id,
                'date': str(transaction.date),
                'quantity': str(transaction.quantity)
            })
        return {'transactions': transactions} if transactions is not None else None

    def backup(self):
        from src.Configuration.Configure import Configuration
        if Configuration().determine_env() == 'LocalTest':
            logging.info('LocalTestMode: cannot backup')

    def db_url_parser(self):
        from os import environ
        import gzip
        from sh import pg_dump

        db_url = environ['DATABASE_URL']
        list = db_url.split('/')[2:]
        user = list[0].split(':')[0]
        port = list[0].split(':')[2]
        host = list[0].split('@')[1].split(':')[0]
        password = list[0].split(':')[1].split('@')[0]
        db = list[1]

        with gzip.open('backup.gz', 'wb') as backup:
            pg_dump('--column-inserts', '-h', host, '-U', user, db, '-p', port, _out=backup)
        return self.dropbox_upload('backup.gz')

    def dropbox_upload(self, backup_file):
        from datetime import date
        from dropbox import Dropbox
        from dropbox.exceptions import AuthError, ApiError
        from dropbox.files import WriteMode
        from os import environ, system

        backup_path = '/backup' + str(date.today()) + '.gz'
        dbx = Dropbox(environ['DROPBOX_API_KEY'])
        logging.info('Uploading ' + backup_file + ' to Dropbox as ' + backup_path)

        try:
            dbx.users_get_current_account()
        except AuthError:
            logging.ERROR('Invalid dropbox token, cannot authenticate')
            return None

        self.remove_old_backups(dbx)

        with open(backup_file, 'rb') as backup:
            try:
                logging.info('Uploading ' + backup_file + ' to Dropbox as ')
                dbx.files_upload(backup.read(), backup_path, mode=WriteMode('overwrite'))
                logging.info('Backup succeded!')
                system('rm', backup_file)
                return True
            except ApiError as err:
                if err.error.is_path() and err.error.get_path().reason.is_insufficient_space():
                    logging.Error('No free space available to Dropbox, cannot backup')
                    system('rm', backup_file)
                    return None
                elif err.user_message_text:
                    logging.ERROR('Cannot backup: ' + err.user_message_text)
                    return None
                else:
                    logging.ERROR(err)
                    return None

    def remove_old_backups(dbx):
        from datetime import date
        try:
            current_year = date.today().year
            dbx.files_delete('/backup' + date.today().replace(year=current_year-1) + '.gz')
            logging.warning('Removed old backup')
            return
        except:
            logging.info('No backup older than a year to be removed')
            return