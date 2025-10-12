import jwt
import bcrypt
import access_db
from flask import current_app
from flask_login import UserMixin
from datetime import datetime, timedelta


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
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8'))


    def generate_token(self):
        payload = {
            'exp': datetime.now().astimezone() + timedelta(days=0, minutes=6),
            'id': self.id
        }
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')


    @staticmethod
    def check_token(token):
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            query_seq = access_db.query(tablename="Users", target={"user_id": data["id"]})
            user = User(id=query_seq[0][0],
                        username=query_seq[0][1],
                        email=query_seq[0][2])
            return user

        except jwt.exceptions.ExpiredSignatureError:
            print("Token has expired")
            return None
