__author__ = 'Mikołaj Henklewski'
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config
from os import path

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.app = app
db.init_app(app)
lm = LoginManager()
lm.init_app(app)
bcrypt = Bcrypt()
CONFIG = Config


app.static_path = path.join(path.abspath(__file__), 'static')


if __name__ == '__main__':
    from views import *
    app.run(debug=CONFIG.DEBUG, host=CONFIG.HOST, port=CONFIG.PORT)
