from .models import User, UserSchema, bc
from flask import request, Blueprint
from flask_jwt_extended import create_access_token

bp = Blueprint('auth', __name__)


@bp.route('/auth', methods=['POST'])
def auth():
    return login_by_json(request.json)


def login_by_json(json):
    if json:
        return validate(json.get('username'), json.get('password'))
    else:
        return {'error': 'no data'}, 400


def validate(username, password):
    if username and password:
        return get_token(username, password)
    else:
        return {'error': 'missing data'}, 401


def get_token(username, password):
    if compare(get_user_hash(username), password):
        return {'access_token': create_access_token(username)}, 200
    else:
        return {'error': 'wrong data'}, 401


def get_user_hash(username):
    return UserSchema().dump(
                User.query.filter_by(username=username).first()
            ).get('password')


def compare(passwd_hash, passwd):
    if passwd_hash and passwd:
        return bc.check_password_hash(passwd_hash, passwd)
    else:
        return False
