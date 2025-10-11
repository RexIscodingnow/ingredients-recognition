from flask import Flask
from flask_login import LoginManager
import config


app = Flask(__name__, template_folder="html")
app.config.from_object(config.Config)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.session_protection = 'strong'

