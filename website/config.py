import os
import dotenv

dotenv.load_dotenv()


class Config:
    SECRET_KEY = 'fjfisljdqoiahf;laojdqahlwdjayfghlkjd'
    JWT_SECRET_KEY = 'CodingProgrammingforsecretkeytokentoken'
    JWT_TOKEN_LOCATION = ['headers', 'query_string']
    SESSION_COOKIE_SECURE = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")


