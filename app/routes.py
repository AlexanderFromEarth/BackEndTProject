import datetime

from flask import request, render_template, redirect, make_response, abort, session
from sqlalchemy.exc import IntegrityError

from . import app, bcrypt, models


@app.route('/')
def main():
    return render_template('index.html')


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
        except IntegrityError:
            models.db.session.rollback()
        finally:
            return redirect('/')
    
    return render_template("registration.html")


@app.route('/users/')
def all_users():
    users = models.User.query.all()
    return render_template('users.html', users=users)


@app.route('/users/<username>', methods=['GET']) 
def user(username):
    user = models.User.query.filter_by(username=username).first()
    cur_user = session.get('name')

    if not user:
        abort(404)

    return render_template('user.html', user=user, cur_user=cur_user)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    cur_user = models.User.query.filter_by(username=session['name']).first()

    if not cur_user:
        abort(404)
    
    if request.method == 'POST':
        if cur_user.check_password(request.form.get('oldpass')):
            cur_user.set_password(request.form.get('newpass'))
            models.db.session.commit()
    
    return render_template('settings.html')


@app.route('/settings/delete_user', methods=['POST'])
def delete():
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


@app.route('/settings/create_artist', methods=['GET', 'POST'])
def create_artist():
    pass


@app.route('/bulletin_board')
def get_list_advertisement():
    pass


@app.route('/bulletin_board/<id>')
def get_ad(id):
    pass


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
