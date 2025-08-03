# apps
from flask import Flask
from config import Config

# database shenanigans
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# login sessions
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

login = LoginManager(app)
login.login_view = 'login' # to be able to do the login required thing

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models

