from .models import Song, SongSchema, db
from flask import request, jsonify, url_for, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError


bp = Blueprint('songs', __name__)
song_schema = SongSchema()
songs_schema = SongSchema(many=True)


@bp.route('/', methods=['GET'])
def main():
    return {
        'songs_url': url_for('songs.songs', _external=True),
        'user_url': url_for('songs.songs', username='', _external=True),
        'cur_song_url': url_for('songs.cur_song', _external=True)
    }


@bp.route('/song', methods=['GET'])
def songs():
    if request.method == 'POST':
        if not request.json:
            return {'error': 'no data'}, 400

        title = request.json.get('title')
        artist = request.json.get('artist')

        song = Song(title=title,
                    artist=artist)


        db.session.add(song)

        try:
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            return {'error': error.args}, 400

        return {}, 201

    return jsonify(songs_schema.dump(Song.query.all())), 200


@bp.route('/song/<title>', methods=['GET'])
def song(title):
    song = Song.query.filter_by(title=title).first()

    if not song:
        return {'error': 'song not found'}, 404

    return song_schema.dump(song), 200


@bp.route('/song', methods=['GET', 'PUT', 'DELETE'])
@jwt_required
def cur_song():
    title = get_jwt_identity()
    song = Song.query.filter_by(title=title).first()

    if not song:
        error_code = 404 if request.method == 'GET' else 204
        return {'error': 'song not found'}, error_code

    if request.method == 'PUT':
        if request.json.get('title'):
            song.title = request.json['title']
        if request.json.get('artist'):
            song.title = request.json['artist']

        try:
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            return {'error': error.args}, 400

        return {}, 200
    elif request.method == 'DELETE':
        db.session.delete(song)

        try:
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            return {'error': error.args}, 400

        return {}, 200

    return song_schema.dump(song), 200
