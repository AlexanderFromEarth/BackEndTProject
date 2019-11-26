from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from marshmallow.exceptions import MarshmallowError
from .models import User, UserSchema, db

bp = Blueprint('users', __name__)


@bp.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        if not request.json:
            return {'error': 'no data'}, 400

        try:
            db.session.add(UserSchema().load(request.json))
            db.session.commit()
        except MarshmallowError as error:
            return {'error': error.args[0]}, 400
        except SQLAlchemyError as error:
            db.session.rollback()
            return {'error': error.args[0]}, 400

        return {}, 201

    return jsonify(UserSchema(exclude=('password',)).dump(
        User.query.all(), many=True
    )), 200


@bp.route('/users/<username>', methods=['GET'])
def user(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return {'error': 'user not found'}, 404

    return UserSchema(exclude=('password',)).dump(user), 200


@bp.route('/user', methods=['GET', 'PUT', 'DELETE'])
@jwt_required
def cur_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return {'error': 'user not found'}, 204

    if request.method == 'PUT':
        if request.json.get('email'):
            user.email = request.json['email']
        if user.check_password(request.json.get(
                                'old_pass')) and request.json.get('new_pass'):
            user.set_password(request.json['new_pass'])

        try:
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            return {'error': error.args}, 400

        return {}, 200
    elif request.method == 'DELETE':
        db.session.delete(user)

        try:
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            return {'error': error.args}, 400

        return {}, 200

    return UserSchema(exclude=('password',)).dump(user), 200
