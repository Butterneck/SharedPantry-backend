from main import db


class Product(db.Model):

    __tablename__ = 'Products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity


    def __str__(self):
        return "[" + str(self.id) + "] " + self.name + "-" + str(self.quantity) + "-" + str(self.price)