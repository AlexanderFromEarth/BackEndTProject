from . import bc, db, ma


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.Binary, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    realname = db.Column(db.String(120), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    registration_date = db.Column(db.Date, nullable=False)
    phone_number = db.Column(db.String, nullable=True)

    def set_password(self, password):
        if password:
            self.password = bc.generate_password_hash(password)

    def check_password(self, password):
        if password:
            return bc.check_password_hash(self.password, password)


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

    url = ma.URLFor('users.user', username='<username>', _external=True)
