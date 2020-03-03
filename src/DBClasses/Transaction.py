from api import db


class Transaction(db.Model):

    __tablename__ = 'Transactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.chat_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


    def __init__(self, user_id, product_id, date, quantity):
        self.user_id = user_id
        self.product_id = product_id
        self.date = date
        self.quantity = quantity
