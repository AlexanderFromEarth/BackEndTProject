from flask import request, Blueprint
from flask_jwt_extended import create_access_token
from .models import User, UserSchema, bc

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
        return get_token(get_user_data(username), password)
    else:
        return {'error': 'missing data'}, 401


def get_token(user, password):
    if compare(user.get('password'), password):
        return {'access_token': create_access_token(user.get('id'))}, 200
    else:
        return {'error': 'wrong data'}, 401


def get_user_data(username):
    return UserSchema().dump(
                User.query.filter_by(username=username).first()
            )


def compare(passwd_hash, passwd):
    if passwd_hash and passwd:
        return bc.check_password_hash(passwd_hash, passwd)
    else:
        return False
