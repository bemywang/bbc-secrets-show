from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

import os
## install python dotenv - to read env variable
# from dotenv import load_dotenv

app = Flask(__name__)

## Load environment variables from .env file -- local use
# load_dotenv()


## ----- os for deployment
app.config['COLOR'] = os.environ.get('COLOR')
print(app.config['COLOR'])

## --- for local env
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# CONNECT TO DB
## -- local development without env variables
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///users.db")


db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


# CREATE TABLE
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template("index.html", logged_in=current_user.is_authenticated)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":

        username = request.form.get('username')
        result = db.session.execute(db.select(User).where(User.username == username))

        # Note, username in db is unique so will only have one result.
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that username, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            username=request.form.get('username'),
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("secrets"))

    return render_template("register.html", logged_in=current_user.is_authenticated)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        result = db.session.execute(db.select(User).where(User.username == username))
        user = result.scalar()
        # Email doesn't exist or password incorrect.
        if not user:
            flash("That username does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('secrets'))

    return render_template("login.html", logged_in=current_user.is_authenticated)


@app.route('/secrets')
@login_required
def secrets():
    print(current_user.username)
    return render_template("secrets.html", username=current_user.username, logged_in=True)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download')
@login_required
def download():

    # return send_from_directory('/static/files/', 'cheat_sheet.pdf')
    return send_from_directory('static', path="files/secrets.pdf")


if __name__ == "__main__":
    app.run(debug=False)
