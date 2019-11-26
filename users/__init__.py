from flask import Flask
from flask_jwt_extended import JWTManager
from .routes import bp
from .models import bc, db, ma

app = Flask(__name__)
app.config.from_object('config')

jwt = JWTManager(app)

bc.init_app(app)
db.init_app(app)
ma.init_app(app)

db.create_all(app=app)

app.register_blueprint(bp)
