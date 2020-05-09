from werkzeug.exceptions import InternalServerError
from flask import Blueprint, request, redirect, url_for
from flask_login import current_user

from models import Session, Comment, User

comments_app = Blueprint('comments_app', __name__)


@comments_app.route('/', endpoint='index')
def index():
    return redirect(url_for('app.index'))


def create_comment(comment: Comment) -> None:
    Session.add(comment)
    try:
        Session.commit()
    except Exception as e:
        Session.rollback()
        raise InternalServerError(f"Could not create comment! Error: {e}")


@comments_app.route('/<int:data>/add/', endpoint='add_comment',
                    methods=('GET', 'POST',))
def add_comment(data=None):
    comment_text = request.form.get('comment_text')
    user_id = (
        Session.query(User.id)
        .filter(User.username == current_user.username)
        .one_or_none()
    )
    new_comment = Comment(user_id=user_id[0], receipt_id=data,
                          text=comment_text)
    create_comment(new_comment)
    return redirect(url_for("receipts_app.receipt_info", data=data))
