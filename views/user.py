from werkzeug.exceptions import BadRequest, InternalServerError
from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import current_user, login_required

from models import Session, User

users_app = Blueprint('users_app', __name__)


@users_app.route('/', endpoint='index')
def index():
    users = Session.query(User).limit(25)
    return render_template("users/index.html", users=users)


@users_app.route('/current/profile/', endpoint='current', methods=('GET', 'POST'))
def current():
    return render_template("users/user.html", user=current_user)


@users_app.route('/<string:data>/profile/', endpoint='user_info', methods=('GET', 'POST'))
def user_profile(data=None):
    user = Session.query(User).filter(User.username == data).one_or_none()

    if not user:
        return redirect(url_for("users_app.current"))

    return render_template("users/user.html", user=user)
