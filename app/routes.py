import datetime

from flask import request, render_template

from app import app


@app.route('/')
def main():
    return render_template("index.html")

@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
       pass
    return render_template('login.html')

@app.route('/registration') 
def registration(): 
    return render_template("registration.html") 

@app.route('/users')
def all_users():
    pass

@app.route('/users/<id>') 
def get_user(): 
    return render_template("my_page.html", 
    name="Alex", 
    surname="Gas", 
    mail="megapoc@mail.ru")

@app.route('/users/<id>/settings')
def settings():
    pass

@app.route('/artists')
def get_all_artists():
    pass

@app.route('/artists/<id>')
def get_artist():
    pass

@app.route('/bulletin_board')
def get_list_advertisement():
    pass

@app.route('/bulletin_board/<id>')
def get_ad():
    pass

@app.route('/articles')
def get_all_articles():
    pass

@app.route('/articles/<id>')
def get_article():
    pass

@app.route('/songs')
def get_all_songs():
    pass

@app.route('/songs/<int:id>',methods = ['GET','POST'])
def song(id):
    if request.method == 'GET':
      return render_template("song.html",author ='Константин',title = 'Берет гитару',song_duration = '300',publication_date = datetime.date(2019,3,5))
    elif request.method == 'POST':
      return render_template("song.html",author ='Константин',title = 'Берет гитару',song_duration = '300',publication_date = datetime.date(2019,3,5))
