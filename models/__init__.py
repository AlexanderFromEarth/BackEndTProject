import os

from flask_sqlalchemy import SQLAlchemy

from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test.db'))

db = SQLAlchemy(app)