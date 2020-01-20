from sqlalchemy import Column, Integer, String, Boolean
from src.db_manager import Base


class User(Base):

    __tablename__ = 'Users'

    chat_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    is_admin = Column(Boolean)

    def __init__(self, chat_id, username):
        self.chat_id = chat_id
        self.username = username,
        self.is_admin = False
