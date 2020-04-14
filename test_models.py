import pytest
from database import Session
from models import Post, Comment, User
from models import Ingredient, IngredientsAssociation


@pytest.fixture
def omelet_ingredients():
    return ['молоко', 'яйцо', 'соль', 'перец', 'бекон']


@pytest.fixture
def all_users():
    return ['Fat Larry', 'Fragrant pepper', 'Child of spices']


def test_all_users(all_users):
    session = Session()
    users = session.query(User).all()
    assert len(users) == 3
    for user in users:
        assert user.username in all_users
    session.close()


def test_pepper_user():
    session = Session()
    user = session.query(User).filter(
        User.username == 'Fragrant pepper').first()
    assert isinstance(user, User)
    assert user.username == 'Fragrant pepper'
    session.close()


def test_larry_posts():
    session = Session()
    user = session.query(User).filter(
        User.username == 'Fat Larry').first()
    posts = user.posts
    assert len(posts) == 2
    session.close()


def test_all_posts():
    session = Session()
    posts = session.query(Post).all()
    assert len(posts) == 4
    session.close()


def test_chicken_post_comments():
    session = Session()
    post = session.query(Post).filter(
        Post.title == 'Курица с овощами').first()
    comments = post.comments
    assert len(comments) == 1
    assert isinstance(comments[0], Comment)
    assert comments[0].text == 'Very nice, Bro!'
    session.close()


def test_ingredients_count_in_post():
    session = Session()
    post = session.query(Post).filter(Post.title == 'Омлет').first()
    ingredients = post.ingredients
    assert len(ingredients) == 5
    assert isinstance(ingredients[0], IngredientsAssociation)
    assert isinstance(ingredients[0].ingredient, Ingredient)
    session.close()


def test_ingredients_in_omelet(omelet_ingredients):
    session = Session()
    post = session.query(Post).filter(Post.title == 'Омлет').first()
    ingredients_assoc = post.ingredients
    for ingredient_assoc in ingredients_assoc:
        assert ingredient_assoc.ingredient.name in omelet_ingredients
    session.close()
