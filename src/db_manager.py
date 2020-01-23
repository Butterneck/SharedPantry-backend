from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class DB_Manager():

    def __init__(self, db_url):
        self.engine = create_engine(db_url)

        # Need to import those classes after Base declaration to avoid importing errors
        from src.DBClasses.User import User as User
        from src.DBClasses.Product import Product
        from src.DBClasses.Transaction import Transaction
        from src.DBClasses.Activator import Activator
        from src.DBClasses.Backup import Backup
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
            'quantity': product.quantity
            }
        }

    def editQuantity(self, product_id, qt):
        from src.DBClasses.Product import Product
        session = self.Session()
        product = session.query(Product).filter_by(id=product_id).first()
        product.quantity = qt
        session.commit()
        return {'product': {
            'id': product.id,
            'name': product.name,
            'quantity': product.quantity
            }
        } if product is not None else None

    def addTransaction(self, chat_id, product_id, qt):
        from src.DBClasses.Transaction import Transaction
        from datetime import date
        if not self.checkAvailability(product_id):
            return None
        transaction = Transaction(chat_id, product_id, date.today(), qt)
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
        print(user)
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
        return {'users': users}  if users is not None else None

    def activateActivator(self):
        from src.DBClasses.Activator import Activator
        session = self.Session()
        activator = session.query(Activator).first()
        activator.activator = True
        session.commit()
        return {'activator': activator.activator}  if activator is not None else None

    def deactivateActivator(self):
        from src.DBClasses.Activator import Activator
        session = self.Session()
        activator = session.query(Activator).first()
        activator.activator = False
        session.commit()
        return {'activator': activator.activator} if activator is not None else None

    def checkActivator(self):
        from src.DBClasses.Activator import Activator
        session = self.Session()
        activator = session.query(Activator).first()
        return {'activator': activator.activator} if activator is not None else None

    def activateBackup(self):
        from src.DBClasses.Backup import Backup
        session = self.Session()
        backup= session.query(Backup).first()
        backup.backup = True
        session.commit()
        return {'backup': backup.backup} if backup is not None else None

    def deactivateBackup(self):
        from src.DBClasses.Backup import Backup
        session = self.Session()
        backup = session.query(Backup).first()
        backup.backup = False
        session.commit()
        return {'backup': backup.backup} if backup is not None else None

    def checkBackup(self):
        from src.DBClasses.Backup import Backup
        session = self.Session()
        backup = session.query(Backup).first()
        return {'backup': backup.backup} if backup is not None else None

    def getAcquistiIn(self):
        return
