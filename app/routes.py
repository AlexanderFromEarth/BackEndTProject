from app import app
from flask import request
from flask import render_template
import datetime


@app.route('/')
def main():
    return render_template("index.html")

@app.route('/login', methods = ['GET','POST'])
def login():
    pass

@app.route('/registration') 
def registration(): 
    return render_template("registration.html") 

@app.route('/users')
def all_users():
    list_users = [{'realname':'Костя','username':'Константин'}, {'realname':'Пуська', 'username':'Пусь'}]
    return render_template("list_users.html", users = list_users)

@app.route('/users/<id>') 
def get_user(id): 
    return render_template("my_page.html", 
    name="Alex", 
    surname="Gas", 
    mail="megapoc@mail.ru")

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
