from datetime import date
from .models import User, UserSchema, db
from flask import request, jsonify, url_for, Blueprint
from sqlalchemy.exc import SQLAlchemyError


bp = Blueprint('users', __name__)
user_schema = UserSchema(exclude=('password',))
users_schema = UserSchema(exclude=('password',),
                          many=True)


@bp.route('/', methods=['GET'])
def main():
    return {
        'users_url': url_for('users.users', _external=True),
        'user_url': url_for('users.user', username='', _external=True)
    }


@bp.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        if not request.json:
            return {'error': 'no data'}, 400

        username = request.json.get('username')
        password = request.json.get('password')
        email = request.json.get('email')
        realname = request.json.get('realname')
        phone_number = request.json.get('phone_number')
        birth_date = request.json.get('birth_date')

        user = User(username=username,
                    realname=realname,
                    email=email,
                    phone_number=phone_number,
                    birth_date=birth_date,
                    registration_date=date.today())
        user.set_password(password)

        db.session.add(user)

        try:
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            return {'error': error.args}, 400

        return {}, 201

    return jsonify(users_schema.dump(User.query.all())), 200


@bp.route('/users/<username>', methods=['GET', 'PUT', 'DELETE'])
def user(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        error_code = 404 if request.method == 'GET' else 204
        return {'error': 'user not found'}, error_code

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

    return user_schema.dump(user), 200
