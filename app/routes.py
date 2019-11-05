import datetime

from flask import request, render_template, redirect, make_response, abort, session
from sqlalchemy.exc import IntegrityError

from . import app, bcrypt, lm, models


@app.route('/', methods=['GET'])
def main():
    articles=models.Article.query.all()
    return render_template('index.html', articles=articles)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = models.User.query.filter_by(username=request.form.get('login')).first()

        if not user:
            abort(404) # Need to change

        if user.check_password(request.form.get('password')):
            session['name'] = user.username
            return redirect('/users/{}'.format(user.username))
        else:
            abort(404)
    elif request.method == 'GET':
        return render_template('login.html')


@app.route('/logout')
def logout():
    if session.get('name'):
        del session['name']

    return redirect('/')


@app.route('/registration', methods=['GET', 'POST']) 
def registration():
    if request.method == "POST":
        user = models.User(username=request.form.get('login'), 
                           password=bcrypt.generate_password_hash(request.form.get('password'), 10),
                           realname=request.form.get('realname'),
                           email=request.form.get('email'))

        if models.User.query.filter_by(username=user.username).first():
            return render_template('registration.html', error='Username already exists')

        if models.User.query.filter_by(email=user.email).first():
            return render_template('registration.html', error='Email already exists')

        models.db.session.add(user)
        
        try:
            models.db.session.commit()
            session['name'] = user.username
        except IntegrityError:
            models.db.session.rollback()
        finally:
            return redirect('/users/{}'.format(user.username))
    
    return render_template("registration.html")


@app.route('/users/')
def all_users():
    users = models.User.query.all()
    return render_template('users.html', users=users)


@app.route('/users/<username>', methods=['GET']) 
def user(username):
    user = models.User.query.filter_by(username=username).first()

    if not user:
        abort(404)

    return render_template('user.html', user=user)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    cur_user = models.User.query.filter_by(username=session.get('name')).first()

    if not cur_user:
        return redirect('/')
    
    if request.method == 'POST':
        if cur_user.check_password(request.form.get('oldpass')):
            cur_user.set_password(request.form.get('newpass'))
            models.db.session.commit()
    
    return render_template('settings.html')


@app.route('/settings/delete_user', methods=['POST'])
def delete_user():
    user = models.User.query.filter_by(username=session.get('name')).first()
    models.db.session.delete(user)

    try:
        models.db.session.commit()

        if session.get('name'):
            del session['name']
    except IntegrityError:
        models.db.session.rollback()
    finally:
        return redirect('/')


@app.route('/artists')
def get_all_artists():
    aritsts = models.Artist.query.all()
    return render_template('artists.html', artists=aritsts)


@app.route('/artists/<id>')
def get_artist(id):
    artist = models.Artist.query.filter_by(id=id).first()

    if not artist:
        abort(404)

    return render_template('artist.html', artist=artist)

@app.route('/artists/<id>/change', methods = ['GET','POST'])
def change_artist(id):
    artist = models.Artist.query.filter_by(id=id).first()

    if not artist:
        abort(404)
    
    if request.method == 'GET':
        return render_template('change_artist.html', artist=artist)
    elif request.method == 'POST':
        artist.name = request.form.get('name')
        models.db.session.commit()
        return redirect('/artists/{}'.format(artist.id))

@app.route('/artists/<id>/change/add_member', methods = ['GET','POST'])   
def add_member(id):
    artist = models.Artist.query.filter_by(id=id).first()

    if request.method == 'POST':
        user = models.User.query.filter_by(username = request.form.get('name')).first()
        if not user:
            return render_template('add_member.html', error='There is no user with this number',artist=artist)
        artist.members.append(user)        
        models.db.session.commit()
        return redirect('/artists/{}'.format(artist.id))
    elif request.method == 'GET':
        return render_template('add_member.html',artist=artist)

@app.route('/artists/<id>/change/delete_member', methods = ['GET','POST'])   
def delete_member(id):
    artist = models.Artist.query.filter_by(id=id).first()

    if request.method == 'GET':
        return render_template('delete_member.html',artist=artist)
    elif request.method == 'POST':
        user = models.User.query.filter_by(username = request.form.get('name')).first()
        if not user:
            return render_template('add_member.html', error='There is no user with this number',artist=artist)
        artist.members.remove(user)        
        models.db.session.commit()
        return redirect('/artists/{}'.format(artist.id))

@app.route('/artists/create_artist', methods=['GET', 'POST'])
def create_artist():
    if request.method == 'POST':        
        cur_user = models.User.query.filter_by(username=session.get('name')).first()
        if not cur_user:
            return redirect('/')
        artist = models.Artist(name = request.form.get('name'),
                               creation_date = datetime.date.today())

        if models.Artist.query.filter_by(name= artist.name).first():
            return render_template('add_artist.html', error='Name already exists')
        artist.members.append(cur_user)
        models.db.session.add(artist)
        
        try:
            models.db.session.commit()
        except IntegrityError:
            models.db.session.rollback()
        finally:
            return redirect('/artists')
    return render_template('add_artist.html')

@app.route('/artists/<id>/settings/delete_artist', methods=['POST'])
def delete_artist(id):
    artist = models.Artist.query.filter_by(id=id).first()
    models.db.session.delete(artist)

    try:
        models.db.session.commit()
    except IntegrityError:
        models.db.session.rollback()
    finally:
        return redirect('/artists')


@app.route('/articles')
def articles():
    articles = models.Article.query.all()
    return render_template('articles.html', articles=articles)


@app.route('/bulletins/')
def bulletins():
    bulletins = models.Bulletin.query.all()
    return render_template('bulletins.html', bulletins=bulletins)


@app.route('/articles/create', methods=['GET', 'POST'])
def create_article():
    if request.method == 'GET':
        return render_template('create_article.html')
    elif request.method == 'POST':
        article = models.Article(
            title=request.form.get('title'),
            text=request.form.get('text'),
            user=models.User.query.filter_by(username=session.get('name')).first()
        )
        try:
            models.db.session.commit()
        except IntegrityError:
            models.db.session.rolback()
        finally:
            return redirect(f'/articles/{article.id}')


@app.route('/bulletins/create', methods=['GET', 'POST'])
def create_bulletin():
    if not session.get('name'):
        return redirect('/bulletins')

    if request.method == 'GET':
        return render_template('create_bulletin.html', roles=models.Role.query.all())
    elif request.method == 'POST':
        bulletin = models.Bulletin(title=request.form.get('title'), 
                                   text=request.form.get('text'), 
                                   user=models.User.query.filter_by(username=session.get('name')).first(),
                                   role=models.Role.query.filter_by(name=request.form.get('role')).first())
        
        try:
            models.db.session.commit()
        except IntegrityError:
            models.db.session.rollback()
        finally:
            return redirect('/bulletins/{}'.format(bulletin.id))


@app.route('/articles/<id>', methods=['GET'])
def article(id):
    article = models.Article.query.filter_by(id=id).first()

    if not article:
        abort(404)

    return render_template('article.html', article=article)


@app.route('/bulletins/<id>', methods=['GET'])
def bulletin(id):
    bulletin = models.Bulletin.query.filter_by(id=id).first()

    if not bulletin:
        abort(404)

    return render_template('bulletin.html', bulletin=bulletin)


@app.route('/articles/<id>/change', methods=['GET', 'POST'])
def change_articles(id):
    article = models.Article.query.filter_by(id=id).first()

    if not bulletin:
        abort(404)

    if request.method == 'GET':
        return render_template('change_articles.html', article=article)
    elif request.method == 'POST':
        article.title = request.form.get('title')
        article.text = request.form.get('text')

        models.db.session.commit()

        return redirect(f'/articles/{article.id}')


@app.route('/bulletins/<id>/change', methods=['GET', 'POST'])
def change_bulletins(id):
    bulletin = models.Bulletin.query.filter_by(id=id).first()

    if not bulletin:
        abort(404)
    
    if request.method == 'GET':
        return render_template('change_bulletin.html', bulletin=bulletin)
    elif request.method == 'POST':
        bulletin.title = request.form.get('title')
        bulletin.text = request.form.get('text')
        bulletin.role = request.form.get('role')

        models.db.session.commit()

        return redirect(f'/bulletins/{bulletin.id}')


@app.route('/articles/<id>/delete', methods=['POST'])
def delete_articles(id):
    article = models.Article.query.filter_by(id=id).first()

    if not article:
        abort(404)

    if session.get('name') != article.user.username:
        return redirect(f'/articles/{article.id}')

    models.db.session.delete(article)

    try:
        models.db.session.commit()
    except IntegrityError:
        models.db.session.rollback()
    finally:
        return redirect('/articles')


@app.route('/bulletins/<id>/delete', methods=['POST'])
def delete_bulletins(id):
    bulletin = models.Bulletin.query.filter_by(id=id).first()

    if not bulletin:
        abort(404)
    
    if session.get('name') != bulletin.user.username:
        return redirect(f'/bulletins/{bulletin.id}')
    
    models.db.session.delete(bulletin)

    try:
        models.db.session.commit()
    except IntegrityError:
        models.db.session.rollback()
    finally:
        return redirect('/bulletins')


@app.route('/articles')
def get_all_articles():
    pass


@app.route('/articles/<id>')
def get_article(id):
    pass


@app.route('/songs')
def get_all_songs():
    pass


@app.route('/songs/<int:id>', methods = ['GET','POST'])
def song(id):
      return render_template(
          "song.html",author ='Константин',title = 'Берет гитару',song_duration = '300',publication_date = datetime.date(2019,3,5))


@app.route('/songs/add_song')
def add_song():
      return render_template("song.html",author ='Константин',title = 'Берет гитару',song_duration = '300',publication_date = datetime.date.today())
