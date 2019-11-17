from . import bc, db, ma


class Song(db.Model):
    __tablename__ = 'songs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'),
                          nullable=False)
    artist = db.relationship('Artist', backref=db.backref('songs',
                                                          lazy='dynamic'))


class SongSchema(ma.ModelSchema):
    class Meta:
        model = Song

    url = ma.URLFor('songs.song', songtitle='<songtitle>', _external=True)
