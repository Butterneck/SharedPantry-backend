from sqlalchemy import Column, Integer, String
from src.db_manager import Base


class Product(Base):

    __tablename__ = 'Products'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)


    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity


    def __str__(self):
        return "[" + str(self.id) + "] " + self.name + "-" + str(self.quantity) + "-" + str(self.price)