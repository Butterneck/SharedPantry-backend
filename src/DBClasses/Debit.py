from sqlalchemy import Column, Integer, Boolean, ForeignKey
from src.db_manager import Base


class Debit(Base):

    __tablename__ = 'Debits'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.chat_id'))
    quantity = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    paid = Column(Boolean, nullable=False)
