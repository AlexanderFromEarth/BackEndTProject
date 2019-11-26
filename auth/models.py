from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
bc = Bcrypt()
ma = Marshmallow()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.Binary, nullable=False)

    def check_password(self, password):
        if self.password and password:
            return bc.check_password_hash(self.password, password)
        else:
            return False


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
