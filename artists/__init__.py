from flask import Flask
from .routes import bp
from .models import db, ma

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)
ma.init_app(app)

db.create_all(app=app)

app.register_blueprint(bp)
