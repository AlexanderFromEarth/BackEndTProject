from flask import request, jsonify, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from .models import Artist, ArtistSchema, MemberSchema, db

bp = Blueprint('artists', __name__)


@bp.route('/artists', methods=['POST'])
def mkartist() -> (dict, int):
    """
    Creates new artist.

    Args:
        Json in request that matches to ArtistSchema.

    Returns:
        Empty dict and 200 if OK else error message and 400.
    """
    if not request.json:
        return {'error': 'no data'}, 400

    db.session.add(ArtistSchema().load(request.json))
    db.session.flush()

    try:
        db.session.commit()
    except SQLAlchemyError as error:
        db.session.rollback()
        return {'error': error.args}, 400

    return {}, 200


@bp.route('/artists', methods=['GET'])
def artists() -> (dict, int):
    """
    Returns list of artists.

    Returns:
        Jsonized list of dicts that match to ArtisSchema.
    """
    return jsonify(ArtistSchema().dump(Artist.query.all(), many=True)), 200


@bp.route('/artists/<int:id>', methods=['GET'])
def artist(id: int) -> (dict, int):
    artist = Artist.query.get(id)

    if not artist:
        return {'error': 'data not found'}, 404

    return jsonify(ArtistSchema().dump(artist)), 200


@bp.route('/artists/<int:id>', methods=['PUT', 'DELETE'])
def chartist(id: int) -> (dict, int):
    artist = Artist.query.get(id)

    if not artist:
        return {'error': 'data not found'}, 404

    if request.method == 'PUT':
        if not request.json:
            return {'error': 'no data'}, 400

        members = request.json.get('members')

        if members:
            artist.members.clear()

            for member in members:
                artist.members.append(MemberSchema().load(member))
    elif request.method == 'DELETE':
        db.session.delete(artist)

    try:
        db.session.commit()
    except SQLAlchemyError as error:
        db.session.rollback()
        return {'error': error.args}, 400

    return {}, 200
