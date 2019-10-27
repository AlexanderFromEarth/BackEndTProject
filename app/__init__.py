from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

from . import routes

db = SQLAlchemy(app)

from . import models

db.create_all()