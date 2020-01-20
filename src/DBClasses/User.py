from sqlalchemy import Column, Integer, String
from src.db_manager import Base


class User(Base):

    __tablename__ = 'Users'

    chat_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)

    def __init__(self, chat_id, username):
        self.chat_id = chat_id
        self.username = username,
