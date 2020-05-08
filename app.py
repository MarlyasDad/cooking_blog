from typing import Optional
from flask import Flask, render_template, session, request
from sqlalchemy import or_
from models import Session, User, Receipt, Tag, Category

from flask_login import LoginManager, current_user

from views import auth_app, users_app, receipts_app, comments_app

app = Flask(__name__, static_folder="static")
app.config['SECRET_KEY'] = "wertyuiudo3874g2o91413/f'34/f134f17g893f781foirfgdjhf"

app.register_blueprint(auth_app, url_prefix='/auth')
app.register_blueprint(users_app, url_prefix='/users')
app.register_blueprint(receipts_app, url_prefix='/receipts')
app.register_blueprint(comments_app, url_prefix='/comments')

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Session.query(User).filter_by(id=user_id).one_or_none()


@app.route('/', endpoint="index", methods=('GET', 'POST'))
@app.route('/<string:data>/', methods=('GET', 'POST'))
def index(data=None):
    last_id = 0  # for pagination
    tag_name: Optional[str] = None
    search: Optional[str] = request.args.get('search')
    receipts_query = Session.query(Receipt)
    category_alias: str = data
    category_name: Optional[str] = None
    if category_alias:
        category_query = Session.query(Category)
        # lower() or upper() doesn't work with SQLite.
        category_query = (
            category_query.filter(
                or_(
                    Category.alias == category_alias.lower(),
                    Category.alias == category_alias.title()
                )
            )
        )
        category = category_query.one_or_none()
        category_name = category.name
        receipts_query = receipts_query.filter(Receipt.category == category)

    if tag_name:
        tag_query = Session.query(Tag)
        # lower() or upper() doesn't work with SQLite.
        tag_query = (
            tag_query.filter(
                or_(
                    Tag.name == tag_name.lower(),
                    Tag.name == tag_name.title()
                )
            )
        )
        tag = tag_query.one_or_none()
        receipts_query = receipts_query.filter(Receipt.tags.contains(tag))

    if last_id:
        receipts_query = receipts_query.filter(Receipt.id > last_id)

    if search:
        # lower() or upper() doesn't work with SQLite.
        receipts_query = (
            receipts_query.filter(
                or_(Receipt.title.like(f'%{search.lower()}%'),
                    Receipt.title.like(f'%{search.title()}%'))
            )
        )

    receipts = receipts_query.limit(25)
    return render_template('index.html',
                           receipts=receipts,
                           search=search,
                           category=category_name,
                           user=current_user)


@app.before_request
def session_init(*args):
    if hasattr(current_user, 'username'):
        session.username = current_user.username


@app.teardown_request
def remove_session(*args):
    Session.remove()


if __name__ == '__main__':
    app.run(debug=True)
