from .models import User
from flask import request, Blueprint
from flask_jwt_extended import create_access_token

bp = Blueprint('auth', __name__)


@bp.route('/auth', methods=['POST'])
def auth():
    if not request.json:
        return {'error': 'no data'}, 400

    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        return {'access_token': create_access_token(username)}, 200
    else:
        return {'error': 'bad request'}, 401
