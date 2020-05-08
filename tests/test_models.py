import pytest
from models import Session
from models import Receipt, Comment, User
from models import Ingredient, IngredientsAssociation


def teardown_module(module):
    """ teardown any state that was previously setup with a setup_module
    method."""
    print('Session removed.')
    Session.remove()


@pytest.fixture
def omelet_ingredients():
    return ['специи', 'яйцо', 'соль', 'перец', 'бекон', 'масло оливковое', 'сыр', 'лук']


@pytest.fixture
def all_users():
    return ['Fat Larry', 'Fragrant pepper', 'Child of spices', 'User']


def test_all_users(all_users):
    session = Session()
    users = session.query(User).all()
    assert len(users) >= 4
    session.close()


def test_pepper_user():
    user = Session.query(User).filter(
        User.username == 'Fragrant pepper').first()
    assert isinstance(user, User)
    assert user.username == 'Fragrant pepper'


def test_larry_posts():
    user = Session.query(User).filter(
        User.username == 'Fat Larry').first()
    receipts = user.receipts
    assert len(receipts) >= 2


def test_all_posts():
    posts = Session.query(Receipt).all()
    assert len(posts) >= 4


def test_chicken_post_comments():
    receipt = Session.query(Receipt).filter(
        Receipt.title.like('%Курица%')).first()
    comments = receipt.comments
    assert len(comments) >= 1
    assert isinstance(comments[0], Comment)
    assert comments[0].text == 'Very nice, Bro!'


def test_ingredients_count_in_post():
    receipt = Session.query(Receipt).filter(Receipt.title.like('%Омлет%')).first()
    ingredients = receipt.ingredients
    assert len(ingredients) >= 5
    assert isinstance(ingredients[0], IngredientsAssociation)
    assert isinstance(ingredients[0].ingredient, Ingredient)


def test_ingredients_in_omelet(omelet_ingredients):
    receipt = Session.query(Receipt).filter(Receipt.title.like('%Омлет%')).first()
    ingredients_assoc = receipt.ingredients
    for ingredient_assoc in ingredients_assoc:
        assert ingredient_assoc.ingredient.name in omelet_ingredients
