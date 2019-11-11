from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
bc = Bcrypt(app)
ma = Marshmallow(app)

from .routes import bp

app.register_blueprint(bp)
