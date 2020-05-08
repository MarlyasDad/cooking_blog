from models import Base, Session, User, Receipt, Comment
from models import Ingredient, IngredientsAssociation
from models import Category


def create_users():
    users = [
        User(
            email='user@testdomain.com',
            username='User',
            password='Userpass',
            preferences='Люблю вкусно покушать!',
            avatar=None,
        ),
        User(
            email='larry@testdomain.com',
            username='Fat Larry',
            password='Qwerty123',
            preferences='Сытные мясные блюда и десерты.',
            avatar='larry-small.jpeg',
        ),
        User(
            email='pepper@testdomain.com',
            username='Fragrant pepper',
            password='Qwerty456',
            preferences='Блюда из овощей и фруктов.',
            avatar='pepper-small.jpg',
        ),
        User(
            email='spices@testdomain.com',
            username='Child of spices',
            password='Qwerty789',
            preferences='Ароматные специи.',
            avatar='spices-small.jpeg',
        ),
    ]
    Session.add_all(users)
    Session.commit()


def create_ingredients():
    ingredients = [
        Ingredient(name='яйцо'),
        Ingredient(name='масло сливочное'),
        Ingredient(name='масло оливковое'),
        Ingredient(name='лук'),
        Ingredient(name='сыр'),
        Ingredient(name='молоко'),
        Ingredient(name='сахар'),
        Ingredient(name='банан'),
        Ingredient(name='шоколад'),
        Ingredient(name='соль'),
        Ingredient(name='перец'),
        Ingredient(name='курица'),
        Ingredient(name='розмарин'),
        Ingredient(name='специи'),
        Ingredient(name='лёд'),
        Ingredient(name='бекон'),
        Ingredient(name='водка'),
        Ingredient(name='томатный сок'),
    ]
    Session.add_all(ingredients)
    Session.commit()


def create_categories():
    categories = [
        Category(name='Завтраки', alias='breakfasts'),
        Category(name='Вторые блюда', alias='dinners'),
        Category(name='Закуски и салаты', alias='salads'),
        Category(name='Коктейли', alias='cocktails'),
        Category(name='Горячие напитки', alias='drinks'),
        Category(name='Десерты', alias='cakes'),
    ]
    Session.add_all(categories)
    Session.commit()


def create_omelet_post():
    user = Session.query(User).filter(User.username == 'Fat Larry').one_or_none()
    category = Session.query(Category).filter(Category.name == 'Завтраки').one_or_none()
    receipt_text = '''Нагрейте оливковое масло в маленькой сковороде на среднем огне.
        Добавьте лук и бекон, жарьте 2-3 минуты, постоянно помешивая компоненты.
        Взбейте два яйца, разбавьте небольшим количеством холодной воды.
        Приправьте специями, тщательно перемешайте.
        Постепенно выливайте яичную смесь на сковороду с луком и беконом.
        Жарьте яичницу с беконом на протяжении 3-4 минут, подавайте с французским багетом. Декорируйте листьями
        салата, пряными веточками душистых трав (укропом, петрушкой).
    '''
    receipt = Receipt(user_id=user.id,
                      category_id=category.id,
                      title='Омлет с беконом',
                      text=receipt_text,
                      is_published=True,
                      category=category,
                      picture='omelette.jpeg',
                      picture_min='omelette-small.jpeg',
                      )
    ingredients = [
        ('яйцо', 'куриное', 3, 'шт'),
        ('бекон', 'тонкий', 125, 'гр'),
        ('масло оливковое', '', 1, 'ст. ложка'),
        ('сыр', 'тёртый', 85, 'гр'),
        ('лук', 'красный', 1, 'шт'),
        ('соль', 'по вкусу', 1, 'щепотка'),
        ('перец', 'по вкусу', 1, 'щепотка'),
        ('специи', 'по вкусу', 1, 'щепотка'),
    ]
    for item in ingredients:
        ingredient = Session.query(Ingredient).filter(
            Ingredient.name == item[0]).first()
        a = IngredientsAssociation(correction=item[1], quantity=item[2], measure=item[3])
        a.ingredient = ingredient
        receipt.ingredients.append(a)
    Session.flush()
    Session.add(receipt)
    Session.commit()


def create_chicken_post():
    user = (
        Session.query(User)
        .filter(User.username == 'Child of spices')
        .first())
    category = (
        Session.query(Category)
        .filter(Category.name == 'Вторые блюда')
        .one_or_none()
    )
    receipt_text = '''Голени посолить, поперчить и обжарить до румяной корочки. Уложить в форму, смазанную маслом.
        Помидоры и один сладкий перец нарезать кубиками, другой перец — средними полосками, лук — полукольцами,
        чеснок измельчить.
        Там же, где жарилась курица, обжарить лук, затем добавить помидоры и перец кубиком, готовить на большом огне
        5 минут. Под конец добавить чеснок и листики 1 веточки розмарина (я добавляла сушёный), посолить,
        поперчить.
        Выложить соус на курицу. Сверху положить полоски перца, целые помидорки черри и 2 веточки розмарина.
        Печь около 25 минут при 200 градусах.
    '''
    receipt = Receipt(user_id=user.id,
                      category_id=category.id,
                      title='Курица с овощами',
                      text=receipt_text,
                      is_published=True,
                      category=category,
                      picture='chicken.jpg',
                      picture_min='chicken-small.jpg',
                      )
    ingredients = [
        ('курица', '', 500, 'гр'),
        ('розмарин', 'по вкусу', 1, 'веточка'),
        ('сметана', '', 1, 'столовая ложка'),
        ('соль', 'по вкусу', 1, 'щепотка'),
        ('перец', 'по вкусу', 1, 'щепотка'),
    ]
    for item in ingredients:
        ingredient = Session.query(Ingredient).filter(
            Ingredient.name == item[0]).first()
        a = IngredientsAssociation(correction=item[1], quantity=item[2], measure=item[3])
        a.ingredient = ingredient
        receipt.ingredients.append(a)
    Session.flush()
    Session.flush()
    Session.add(receipt)
    Session.commit()


def create_cocktail_mary_post():
    user = Session.query(User).filter(User.username == 'Fat Larry').first()
    category = (
        Session.query(Category)
        .filter(Category.name == 'Коктейли')
        .one_or_none()
    )
    receipt_text = '''Налить водку и томатный сок в охлаждённый высокий стакан.
        Добавить лимонный сок.
        После по вкусу насыпать перец и соль.
        Всё тщательно перемешать и украсить веточкой сельдерея, можно долькой лимона.
    '''
    receipt = Receipt(user_id=user.id,
                      category_id=category.id,
                      title='Коктейль Кровавая Мэри',
                      text=receipt_text,
                      is_published=True,
                      category=category,
                      picture='mary.jpg',
                      picture_min='mary-small.jpg',
                      )
    ingredients = [
        ('водка', 'охлаждённая', 75, 'мл'),
        ('томатный сок', '', 100, 'мл'),
    ]
    for item in ingredients:
        ingredient = Session.query(Ingredient).filter(
            Ingredient.name == item[0]).first()
        a = IngredientsAssociation(correction=item[1], quantity=item[2], measure=item[3])
        a.ingredient = ingredient
        receipt.ingredients.append(a)
    Session.flush()
    Session.add(receipt)
    Session.commit()


def create_banana_cocktail_post():
    user = (
        Session.query(User)
        .filter(User.username == 'Child of spices')
        .first())
    category = (
        Session.query(Category)
        .filter(Category.name == 'Коктейли')
        .one_or_none()
    )
    receipt_text = '''Бананы очистить, нарезать кусочками, шоколад разломить на несколько частей.
        В кастрюлю влить молоко, положить бананы и поставить на медленный огонь.
        Постоянно помешивая, довести почти до кипения.
        Как только шоколад расплавится, снять с огня.
        Блендером взбить полученную смесь до появления пены.
        Разлить по стаканам и посыпьте корицей.
    '''
    receipt = Receipt(user_id=user.id,
                      category_id=category.id,
                      title='Молочный коктейль с бананом и шоколадом',
                      text=receipt_text,
                      is_published=True,
                      category=category,
                      picture='banana.jpg',
                      picture_min='banana-small.jpg',
                      )
    ingredients = [
        ('молоко', '', 500, 'мл'),
        ('банан', 'свежий', 1, 'шт'),
        ('шоколад', 'молочный', 80, 'гр'),
        ('сахар', 'по вкусу', 2, 'столовые ложки'),
    ]
    for item in ingredients:
        ingredient = Session.query(Ingredient).filter(
            Ingredient.name == item[0]).first()
        a = IngredientsAssociation(correction=item[1], quantity=item[2], measure=item[3])
        a.ingredient = ingredient
        receipt.ingredients.append(a)
    Session.flush()
    Session.add(receipt)
    Session.commit()


def create_comments_for_receipts():
    user = Session.query(User).filter(
        User.username == 'Fat Larry').first()
    receipt = Session.query(Receipt).filter(
        Receipt.title == 'Курица с овощами').one_or_none()
    comment = Comment(user=user, receipt=receipt, text='Very nice, Bro!')
    Session.add(comment)
    Session.commit()


if __name__ == "__main__":
    Base.metadata.create_all()
    create_users()
    create_ingredients()
    create_categories()
    create_omelet_post()
    create_chicken_post()
    create_cocktail_mary_post()
    create_banana_cocktail_post()
    create_comments_for_receipts()
    Session.remove()



