import bcrypt
from flask_login import UserMixin
from recommend_sys.access_db import cursor, select


class User(UserMixin):
    def __init__(self, username: str, email: str, password: str = "", id: int = None):
        self.username = username
        self.email = email
        self.password = password
        self.id = id

    @property
    def password(self):
        raise AttributeError("password is not readable attribute!!")

    @password.setter
    def password(self, password: str):
        self.hashed_password = self.hash_password(password)


    def hash_password(self, password: str):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')


    def verify_password(self, password: str):
        print(password, self.hashed_password)
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8'))



