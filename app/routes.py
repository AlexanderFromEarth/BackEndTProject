import datetime

from flask import request, render_template, session, jsonify

from . import app, bcrypt, models


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/login', methods=['PUT'])
def login():
    user = models.User.query.filter_by(
        username=request.json.get('login')
        ).first()

    if not user:
        return ({'error': 'user is not defined'},
                400,
                {'content-type': 'application/json'})

    if not user.check_password(request.json.get('password')):
        return ({'error': 'email is not defined'},
                400,
                {'content-type': 'application/json'})

    session['username'] = user.username
    return {}, 200, {'content-type': 'application/json'}


@app.route('/logout')
def logout():
    if session.get('name'):
        del session['name']

    return {}, 200, {'content-type': 'application/json'}


@app.route('/registration', methods=['POST'])
def registration():
    user = models.User(username=request.json.get('login'),
                       password=bcrypt.generate_password_hash(
                           request.json.get('password'),
                           10),
                       realname=request.json.get('realname'),
                       email=request.json.get('email'))

    if models.User.query.filter_by(username=user.username).first():
        return ({'error': 'username already exists'},
                400,
                {'content-type': 'application/json'})

    if models.User.query.filter_by(email=user.email).first():
        return ({'error': 'email already exists'},
                400,
                {'content-type': 'application/json'})

    models.db.session.add(user)

    models.db.session.commit()
    session['name'] = user.username

    return {}, 200, {'content-type': 'application/json'}


@app.route('/users', methods=['GET'])
def users():
    return ({user.id: {
                'username': user.username,
                'email': user.email,
                'artists': {artist.id: {
                    'name': artist.name
                } for artist in user.artists}
                } for user in models.User.query.all()},
            200, {'content-type': 'application/json'})


@app.route('/users/<username>', methods=['GET', 'PUT', 'DELETE'])
def user(username):
    user = models.User.query.filter_by(username=username).first()

    if not user:
        return ({'error': 'user not found'},
                404,
                {'content-type': 'application/json'})

    if request.method == 'PUT':
        if username != session.get('name'):
            return ({'error': 'not for this user'},
                    400,
                    {'content-type': 'application/json'})

        user = models.User.query.filter_by(username=username).first()

        if request.json.get('email'):
            user.email = request.json['email']
        if user.check_password(request.json.get(
                                'old_pass')) and request.json.get('new_pass'):
            user.set_password(request.json['new_pass'])

        models.db.session.commit()

        return {}, 200, {'content-type': 'application/json'}
    elif request.method == 'DELETE':
        if username != session.get('name'):
            return ({'error': 'not for this user'},
                    400,
                    {'content-type': 'application/json'})

        models.db.session.delete(user)

        models.db.session.commit()
        del session['name']

        return {}, 200, {'content-type': 'application/json'}

    return (jsonify(id=user.id,
                    username=user.username,
                    email=user.email,
                    artists={artist.id: {
                        'name': artist.name
                        } for artist in user.artists}),
            200,
            {'content-type': 'application/json'})


@app.route('/artists', methods=['GET', 'POST'])
def artists():
    if request.method == 'POST':
        if not session.get('name'):
            return ({'error': 'need to be auth'},
                    400,
                    {'content-type': 'application/json'})

        artist = models.Artist(name=request.json.get('name'),
                               creation_date=datetime.date.today())

        if models.Artist.query.filter_by(name=artist.name).first():
            return ({'error': 'name already exists'},
                    400,
                    {'content-type': 'application/json'})

        artist.members.append(models.User.query.filter_by(
                                            username=session['name']).first())
        models.db.session.add(artist)

        models.db.session.commit()

        return {}, 200, {'content-type': 'application/json'}

    return ({artist.id: {
                'name': artist.name,
                'users': {user.id: {
                    'id': artist.id,
                    'name': artist.name
                    } for user in artist.users
                    }} for artist in models.Artist.query.all()},
            200, {'content-type': 'application/json'})


@app.route('/artists/<id>', methods=['GET', 'PUT', 'DELETE'])
def artist(id):
    artist = models.Artist.query.filter_by(id=id).first()

    if not artist:
        return ({'error': 'artist not found'},
                404,
                {'content-type': 'application/json'})

    if request.method == 'PUT':
        if session.get['name'] not in [user.username for user in artist.users]:
            return ({'error': 'not for this user'},
                    400,
                    {'content-type': 'application/json'})

        if request.json.get('name'):
            artist.name = request.json['name']
        if request.json.get('members'):
            try:
                for member in request.json['members']:
                    user = models.User.query.filter_by(username=member).first()

                    if user:
                        artist.members.add(user)
            except TypeError as e:
                return ({'error': e},
                        400,
                        {'content-type': 'application/json'})

        return {}, 200, {'content-type': 'application/json'}
    elif request.method == 'DELETE':
        if session.get['name'] not in [user.username for user in artist.users]:
            return ({'error': 'not for this user'},
                    400,
                    {'content-type': 'application/json'})

        models.db.session.delete(artist)

        models.db.session.commit()

        return {}, 200, {'content-type': 'application/json'}
    return (jsonify(id=artist.id,
                    name=artist.name,
                    users={user.id: {
                        'username': user.username,
                        'email': user.email
                        } for user in artist.users}),
            200,
            {'content-type': 'application/json'})


@app.route('/articles', methods=['GET', 'POST'])
def articles():
    if request.method == 'POST':
        if not session.get('name'):
            return ({'error': 'need to be auth'},
                    400,
                    {'content-type': 'application/json'})

        article = models.Article(title=request.json.get('title'),
                                 text=request.json.get('text'))

        if models.Article.query.filter_by(title=article.title).first():
            return ({'error': 'title already exists'},
                    400,
                    {'content-type': 'application/json'})

        article.user.append(models.User.query.filter_by(
                                    username=session['name']).first())
        models.db.session.add(article)

        models.db.session.commit()

        return {}, 200, {'content-type': 'application/json'}

    return ({article.id: {
                'title': article.title,
                'owner': {
                    'id': article.user.id,
                    'name': article.user.name
                    }} for artist in models.Artist.query.all()},
            200, {'content-type': 'application/json'})


@app.route('/bulletins', methods=['GET', 'POST'])
def bulletins():
    if request.method == 'POST':
        if not session.get('name'):
            return ({'error': 'need to be auth'},
                    400,
                    {'content-type': 'application/json'})

        bulletin = models.Bulletin(title=request.json.get('title'),
                                   role=models.Role.query.filter_by(
                                       name=request.json.get('role')).first(),
                                   text=request.json.get('text'))

        if models.Article.query.filter_by(title=bulletin.title).first():
            return ({'error': 'title already exists'},
                    400,
                    {'content-type': 'application/json'})

        bulletin.user.append(models.User.query.filter_by(
                                    username=session['name']).first())
        models.db.session.add(bulletin)

        models.db.session.commit()

        return {}, 200, {'content-type': 'application/json'}

    return ({bulletin.id: {
                'title': bulletin.title,
                'role': bulletin.role.name,
                'owner': {
                    'id': bulletin.user.id,
                    'name': bulletin.user.name
                    }} for bulletin in models.Bulletin.query.all()},
            200, {'content-type': 'application/json'})


@app.route('/articles/<id>', methods=['GET', 'PUT', 'DELETE'])
def article(id):
    article = models.Article.query.filter_by(id=id).first()

    if not article:
        return ({'error': 'article not found'},
                404,
                {'content-type': 'application/json'})

    if request.method == 'PUT':
        if session.get['name'] == article.user.username:
            return ({'error': 'not for this user'},
                    400,
                    {'content-type': 'application/json'})

        if request.json.get('title'):
            article.title = request.json['title']
        if request.json.get('text'):
            article.text = request.json['text']

        return {}, 200, {'content-type': 'application/json'}
    elif request.method == 'DELETE':
        if session.get['name'] == article.user.username:
            return ({'error': 'not for this user'},
                    400,
                    {'content-type': 'application/json'})

        models.db.session.delete(article)

        models.db.session.commit()

        return {}, 200, {'content-type': 'application/json'}
    return (jsonify(id=article.id,
                    title=article.title,
                    owner={'id': article.user.id,
                           'username': article.user.username,
                           'email': article.user.email}),
            200,
            {'content-type': 'application/json'})


@app.route('/bulletins/<id>', methods=['GET'])
def bulletin(id):
    bulletin = models.Bulletin.query.filter_by(id=id).first()

    if not bulletin:
        return ({'error': 'bulletin not found'},
                404,
                {'content-type': 'application/json'})

    if request.method == 'PUT':
        if session.get['name'] == bulletin.user.username:
            return ({'error': 'not for this user'},
                    400,
                    {'content-type': 'application/json'})

        if request.json.get('title'):
            bulletin.title = request.json['title']
        if request.json.get('text'):
            bulletin.text = request.json['text']
        if request.json.get('role'):
            role = models.Role.quert.filter_by(
                            name=request.json['role']).first()

            if role:
                bulletin.role = role

        return {}, 200, {'content-type': 'application/json'}
    elif request.method == 'DELETE':
        if session.get['name'] == bulletin.user.username:
            return ({'error': 'not for this user'},
                    400,
                    {'content-type': 'application/json'})

        models.db.session.delete(bulletin)

        models.db.session.commit()

        return {}, 200, {'content-type': 'application/json'}
    return (jsonify(id=bulletin.id,
                    title=bulletin.title,
                    role={'id': bulletin.role.id,
                          'name': bulletin.role.name
                          },
                    owner={'id': bulletin.user.id,
                           'username': bulletin.user.username,
                           'email': bulletin.user.email}),
            200,
            {'content-type': 'application/json'})
