from main import db


class User(db.Model):

    __tablename__ = 'Users'

    chat_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    is_admin = db.Column(db.Boolean)

    def __init__(self, chat_id, username):
        self.chat_id = chat_id
        self.username = username,
        self.is_admin = False
