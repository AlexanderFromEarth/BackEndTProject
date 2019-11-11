from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
bc = Bcrypt(app)
jwt = JWTManager(app)

from .routes import bp

app.register_blueprint(bp)
