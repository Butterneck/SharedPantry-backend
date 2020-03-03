from api import db

class Debit(db.Model):

    __tablename__ = 'Debits'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.chat_id'))
    quantity = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    paid = db.Column(db.Boolean, nullable=False)
