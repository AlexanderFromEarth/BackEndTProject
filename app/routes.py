import datetime

from flask import request, render_template, redirect, make_response, abort
from sqlalchemy.exc import IntegrityError

from . import app, bcrypt, models


@app.route('/')
def main():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = models.User.query.filter_by(username=request.form.get('login')).first()

        if not user:
            abort(404) # Need to change

        if bcrypt.check_password_hash(user.password, request.form.get('password')):
            resp = make_response(redirect('/'))
            resp.set_cookie('username', user.username, 1)
            return resp
        else:
            abort(404)
    elif request.method == 'GET':
        return render_template('login.html')
    

@app.route('/registration', methods=['GET', 'POST']) 
def registration():
    if request.method == "POST":
        user = models.User(username=request.form.get('login'), 
                           password=bcrypt.generate_password_hash(request.form.get('password'), 10),
                           realname=request.form.get('realname'),
                           email=request.form.get('email'))
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
    return render_template("users.html", users=users)

@app.route('/users/<username>') 
def user(username):
    user = models.User.query.filter_by(username=username).first()

    if not user:
        abort(404)

    return render_template("user.html", user=user)

@app.route('/users/<id>/settings')
def settings(id):
    pass

@app.route('/artists')
def get_all_artists():
    pass

@app.route('/artists/<id>')
def get_artist(id):
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
