from flask import Flask, render_template, request
from flask_bcrypt import Bcrypt
import routes as route

app = Flask(__name__)
bcrypt = Bcrypt(app)


@app.route('/')
def main():
    return render_template("index.html")


@app.route('/registration', methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        print(request.form["login"])
        kek = bcrypt.generate_password_hash(request.form["password"], 10)
        print(kek)
        print(bcrypt.check_password_hash(kek, request.form["password"]))
    return render_template("registration.html")


@app.route('/my_page')
def my_page():
    return render_template("my_page.html",
                           realname="Alex",
                           username="Gas",
                           email="megapoc@mail.ru",
                           info="some text")


@app.route('/list_users')
def list_users():
    users = [{'name': "Катя", 'surname': "Бурилова"}]
    return render_template("list_users.html", users=users)


@app.route('/my_song')
def my_song():
    return render_template("song.html")


@app.route('/add_song')
def add_song():
    return render_template("add_song.html")


if __name__ == '__main__':
    app.run()

