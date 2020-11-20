from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '40702441b4d60a037091caa7349a0dac'
POSTGRES = {
    'user': 'postgres',
    'pw': 'password',
    'db': 'model_repository',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://" + POSTGRES['user'] + ":" + \
    POSTGRES['pw'] + "@" + POSTGRES['host'] + ":" + POSTGRES['port'] + "/" + POSTGRES['db']

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SQLALCHEMY_ECHO'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

db.create_all()

from validation_app import routes