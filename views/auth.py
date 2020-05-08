from werkzeug.exceptions import BadRequest, InternalServerError
from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required

from models import Session, User

auth_app = Blueprint('auth_app', __name__)


@auth_app.route('/', endpoint='index')
def index():
    return render_template("auth/index.html", user=current_user)


def validate_data(username, password):
    if (
            username
            and len(username) >= 3
            and password
            and len(password) >= 8
    ):
        return True


def validate_email_unique(email: str) -> bool:
    if Session.query(User).filter_by(email=email).count():
        return False
    return True


def get_username_and_password():
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")

    return email, username, password


@auth_app.route('/register/', methods=('GET', 'POST'), endpoint='register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for("auth_app.index"))

    if request.method == "GET":
        return render_template("auth/register.html")

    email, username, password = get_username_and_password()
    if not validate_data(username, password):
        return render_template("auth/register.html",
                               error_text="Username has to be at least 3 symbols and password minimum 8")

    if not validate_email_unique(email):
        return render_template("auth/register.html", error_text="Регистрация невозможна!")

    user = User(email, username, password)
    Session.add(user)

    try:
        Session.commit()
    except Exception as e:
        Session.rollback()
        # logger.exception("Error creating user!!")
        raise InternalServerError(f"Could not create user! Error: {e}")

    login_user(user)
    return redirect(url_for("auth_app.index"))


@auth_app.route("/login/", methods=("GET", "POST"), endpoint="login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index", user=current_user))

    if request.method == "GET":
        return render_template("auth/login.html")

    email, username, password = get_username_and_password()
    user = Session.query(User).filter_by(
        email=email
    ).one_or_none()

    print(user, username, password, email)

    if not user or user.password != User.hash_password(password):
        return render_template(
            "auth/login.html",
            error_text="Неправильное имя пользователя или пароль!")

    login_user(user)
    return redirect(url_for("index", user=current_user))


@auth_app.route("/logout/", endpoint="logout")
def logout():
    logout_user()
    return redirect(url_for("index", user=current_user))


@auth_app.route('/<string:data>/profile/', methods=('GET', 'POST'))
def user_profile(data=None):
    return redirect(url_for("auth_app.index"))

