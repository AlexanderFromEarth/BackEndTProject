from . import db, ma


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    creation_date = db.Column(db.Date, nullable=True)

    def is_member(self, id):
        return id in [member.user_id for member in self.members]


class Member(db.Model):
    __tablename__ = 'members'

    artist_id = db.Column('artistID', db.Integer,
                          db.ForeignKey('artists.id'),
                          primary_key=True)
    user_id = db.Column('userID', db.Integer,
                        primary_key=True)
    artist = db.relationship(Artist,
                             backref=db.backref('members',
                                                cascade="""save-update, merge,
                                                delete, delete-orphan"""),
                             uselist=False)


class MemberSchema(ma.ModelSchema):
    class Meta:
        model = Member


class ArtistSchema(ma.ModelSchema):
    class Meta:
        model = Artist

    members = ma.Nested(MemberSchema, many=True, exclude=('artist',))
