from sqlalchemy import Column, Integer, DateTime, ForeignKey
from src.db_manager import Base


class Transaction(Base):

    __tablename__ = 'Transactions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.chat_id'), nullable=False)
    product_id = Column(Integer, ForeignKey('Products.id'), nullable=False)
    date = Column(DateTime, nullable=False)
    quantity = Column(Integer, nullable=False)


    def __init__(self, user_id, product_id, date, quantity):
        self.user_id = user_id
        self.product_id = product_id
        self.date = date
        self.quantity = quantity
