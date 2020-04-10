from sqlalchemy import create_engine, Column, Table, ForeignKey
from sqlalchemy import Integer, String, Text, Boolean
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///cooking_blog.db')
Base = declarative_base(bind=engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


posts_tags_table = Table(
    'posts_tags',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)


class IngredientsAssociation(Base):
    __tablename__ = 'posts_ingredients'

    post_id = Column(Integer, ForeignKey('posts.id'), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'),
                           primary_key=True)
    quantity = Column(Integer)
    ingredient = relationship("Ingredient", back_populates="posts")
    post = relationship("Post", back_populates="ingredients")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False)

    posts = relationship('Post', back_populates='user')
    comments = relationship('Comment', back_populates='user')

    def __repr__(self):
        return f'<User #{self.id} {self.username}>'


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    title = Column(String(40), nullable=False)
    text = Column(Text, nullable=False)
    is_published = Column(Boolean, nullable=False, default=False)

    user = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post')
    tags = relationship('Tag', secondary=posts_tags_table,
                        back_populates='posts')

    ingredients = relationship('IngredientsAssociation',
                               back_populates='post')

    def __repr__(self):
        return f'<Post #{self.id} {self.user_id} {self.title}>'


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False)

    posts = relationship('Post', secondary=posts_tags_table,
                         back_populates='tags')

    def __repr__(self):
        return f'<Tag #{self.id} {self.name}>'


class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    measure = Column(String(10), nullable=False)

    posts = relationship('IngredientsAssociation',
                         back_populates='ingredient')

    def __repr__(self):
        return f'<Ingredient #{self.id} {self.name} {self.measure}>'


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    post_id = Column(Integer, ForeignKey(Post.id), nullable=False)
    text = Column(Text, nullable=False)

    user = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')

    def __repr__(self):
        return f'<Comment #{self.id} {self.user_id} {self.post_id}>'


def create_ingredients():
    session = Session()
    ingredients = [
        Ingredient(name='яйцо', measure='шт'),
        Ingredient(name='молоко', measure='мл'),
        Ingredient(name='сахар', measure='гр'),
        Ingredient(name='банан', measure='шт'),
        Ingredient(name='шоколад', measure='гр'),
        Ingredient(name='соль', measure='гр'),
        Ingredient(name='перец', measure='гр'),
        Ingredient(name='курица', measure='шт'),
        Ingredient(name='розмарин', measure='гр'),
        Ingredient(name='сметана', measure='мл'),
        Ingredient(name='бекон', measure='шт'),
        Ingredient(name='водка', measure='мл'),
        Ingredient(name='томатный сок', measure='мл'),
    ]
    session.add_all(ingredients)
    session.commit()
    session.close()


def create_users():
    session = Session()
    users = [
        User(username='Fat Larry'),
        User(username='Fragrant pepper'),
        User(username='Child of spices'),
    ]
    session.add_all(users)
    session.commit()
    session.close()


def create_omelet_post():
    session = Session()
    user = session.query(User).filter(User.username == 'Fat Larry').first()
    post_text = 'Рецепт вкусного омлета с беконом'
    post = Post(user_id=user.id,
                title='Омлет',
                text=post_text,
                is_published=True)
    ingredients = [
        ('яйцо', 3),
        ('молоко', 200),
        ('соль', 1),
        ('перец', 1),
        ('бекон', 200),
    ]
    for item in ingredients:
        ingredient = session.query(Ingredient).filter(
            Ingredient.name == item[0]).first()
        a = IngredientsAssociation(quantity=item[1])
        a.ingredient = ingredient
        post.ingredients.append(a)
    tags = [
        Tag(name='Омлет'),
        Tag(name='Завтрак'),
    ]
    session.add_all(tags)
    session.flush()
    for tag in tags:
        post.tags.append(tag)
    session.add(post)
    session.commit()
    session.close()


def create_cocktail_margarita_post():
    session = Session()
    user = session.query(User).filter(User.username == 'Fat Larry').first()
    post_text = 'Рецепт алкогольного коктейля Маргарита'
    post = Post(user_id=user.id,
                title='Коктейль Маргарита',
                text=post_text,
                is_published=True)
    ingredients = [
        ('водка', 50),
        ('томатный сок', 50),
    ]
    for item in ingredients:
        ingredient = session.query(Ingredient).filter(
            Ingredient.name == item[0]).first()
        a = IngredientsAssociation(quantity=item[1])
        a.ingredient = ingredient
        post.ingredients.append(a)
    tags = [
        Tag(name='Спиртное'),
    ]
    session.add_all(tags)
    session.flush()
    for tag in tags:
        post.tags.append(tag)
    session.add(post)
    session.commit()
    session.close()


def create_chicken_post():
    session = Session()
    user = session.query(User).filter(
        User.username == 'Child of spices').first()
    post_text = 'Рецепт вкусной курицы с розмарином'
    post = Post(user_id=user.id,
                title='Курица с розмарином',
                text=post_text,
                is_published=True)
    ingredients = [
        ('курица', 500),
        ('розмарин', 1),
        ('сметана', 1),
        ('соль', 1),
        ('перец', 1),
    ]
    for item in ingredients:
        ingredient = session.query(Ingredient).filter(
            Ingredient.name == item[0]).first()
        a = IngredientsAssociation(quantity=item[1])
        a.ingredient = ingredient
        post.ingredients.append(a)
    tags = [
        Tag(name='Курица'),
        Tag(name='Розмарин'),
    ]
    session.add_all(tags)
    session.flush()
    for tag in tags:
        post.tags.append(tag)
    session.add(post)
    session.commit()
    session.close()


def create_banana_cocktail_post():
    session = Session()
    user = session.query(User).filter(
        User.username == 'Child of spices').first()
    post_text = 'Рецепт молочного коктейля с бананом и шоколадом'
    post = Post(user_id=user.id,
                title='Молочный коктейль с бананом и шоколадом',
                text=post_text,
                is_published=True)
    ingredients = [
        ('молоко', 500),
        ('банан', 1),
        ('шоколад', 80),
        ('сахар', 5),
    ]
    for item in ingredients:
        ingredient = session.query(Ingredient).filter(
            Ingredient.name == item[0]).first()
        a = IngredientsAssociation(quantity=item[1])
        a.ingredient = ingredient
        post.ingredients.append(a)
    tags = [
        Tag(name='Коктейль'),
        Tag(name='Банан'),
    ]
    session.add_all(tags)
    session.flush()
    for tag in tags:
        post.tags.append(tag)
    session.add(post)
    session.commit()
    session.close()


def create_comments_for_receipts():
    session = Session()
    user = session.query(User).filter(
        User.username == 'Fat Larry').first()
    post = session.query(Post).filter(
        Post.title == 'Курица с розмарином').first()
    comment = Comment(user=user, post=post, text='Very nice, Bro!')
    session.add(comment)
    session.commit()
    session.close()


def main():
    Base.metadata.create_all()
    # Uncomment if you need to add test data to the database
    # create_ingredients()
    # create_users()
    # create_omelet_post()
    # create_cocktail_margarita_post()
    # create_chicken_post()
    # create_banana_cocktail_post()
    # create_comments_for_receipts()


if __name__ == "__main__":
    main()
