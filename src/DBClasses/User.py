from main import db


class User(db.Model):

    __tablename__ = 'Users'

    chat_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    lang = db.Column(db.String, nullable=False, default='en')
    is_admin = db.Column(db.Boolean)

    def __init__(self, chat_id, username, lang):
        self.chat_id = chat_id
        self.username = username,
        self.lang = lang,
        self.is_admin = False
