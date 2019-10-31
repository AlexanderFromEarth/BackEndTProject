from . import db, bcrypt


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    text = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('users', lazy='dynamic'))


Member = db.Table('members',
    db.Column('userID', db.Integer, db.ForeignKey('users.id')),
    db.Column('artistID', db.Integer, db.ForeignKey('artists.id'))
)
class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    creation_date = db.Column(db.Date, nullable=True)
    members = db.relationship('User',secondary = Member)

    def is_member(self,name):
        b = False
        for mem in self.members:
            if mem.username == name:
                b = True
        return b


class Song(db.Model):
    __tablename__ = 'songs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    artist = db.relationship('Artist', backref=db.backref('songs', lazy='dynamic'))


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.Binary, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    realname = db.Column(db.String(120), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    phone_number = db.Column(db.String, nullable=True)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.String(2), primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)


class Bulletin(db.Model):
    __tablename__ = 'bulletins'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('bulletins', lazy='dynamic'))
    role_id = db.Column(db.String(2), db.ForeignKey('roles.id'), nullable=True)
    role = db.relationship('Role')
    title = db.Column(db.String(80), nullable=False)
    text = db.Column(db.String, nullable=False)
