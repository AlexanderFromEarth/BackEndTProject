from datetime import date
from .models import Artist, ArtistSchema, Member, MemberSchema, db
from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError


bp = Blueprint('artists', __name__)
artist_schema = ArtistSchema()


@bp.route('/artists', methods=['POST'])
@jwt_required
def mkartist():
    if not request.json:
        return {'error': 'no data'}, 400

    name = request.json.get('name')

    artist = Artist(name=name,
                    creation_date=date.today())

    db.session.add(artist)
    db.session.flush()
    user_id = get_jwt_identity()
    db.session.add(Member(artist_id=artist.id, user_id=user_id))

    try:
        db.session.commit()
    except SQLAlchemyError as error:
        db.session.rollback()
        return {'error': error.args}, 400

    return {}, 200


@bp.route('/artists', methods=['GET'])
def artists():
    return jsonify(artist_schema.dump(Artist.query.all(), many=True)), 200


@bp.route('/artists/<id>', methods=['GET'])
def artist(id):
    artist = Artist.query.get(id)

    if not artist:
        return {'error': 'data not found'}, 404

    return jsonify(artist_schema.dump(artist)), 200


@bp.route('/artists/<id>', methods=['PUT', 'DELETE'])
@jwt_required
def chartist(id):
    artist = Artist.query.get(id)

    if not artist:
        return {'error': 'data not found'}, 404

    user_id = get_jwt_identity()

    if user_id not in [member.user_id for member in artist.members]:
        return {'error': 'bad login'}, 401

    if request.method == 'PUT':
        if not request.json:
            return {'error': 'no data'}, 400

        members = request.json.get('members')

        if members:
            artist.members.clear()

            for member in members:
                artist.members.append(MemberSchema().load(member))

        if request.json.get('name'):
            artist.name = request.json['name']
    elif request.method == 'DELETE':
        db.session.delete(artist)

    try:
        db.session.commit()
    except SQLAlchemyError as error:
        db.session.rollback()
        return {'error': error.args}, 400

    return {}, 200
