import time
from typing import Optional
from sqlalchemy import or_

from models import Session, Ingredient, IngredientsAssociation
from models import Receipt, Category

last_id = 1  # for pagination
ingredient_name: Optional[str] = 'Сыр'
search: Optional[str] = "Омлет"

receipts_query = Session.query(Receipt)
association_query = Session.query(IngredientsAssociation)

category_alias: str = "breakfasts"
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
    receipts_query = receipts_query.filter(Receipt.category == category)
    association_query = (
        association_query.join(IngredientsAssociation.receipt)
        .filter(Receipt.category == category)
    )

if ingredient_name:
    ingredient_query = Session.query(Ingredient)
    # lower() or upper() doesn't work with SQLite.
    ingredient_query = (
        ingredient_query.filter(
            or_(
                Ingredient.name == ingredient_name.lower(),
                Ingredient.name == ingredient_name.title()
            )
        )
    )
    ingredient = ingredient_query.one_or_none()
    receipts_query = (
        receipts_query.join(Receipt.ingredients)
        .filter(IngredientsAssociation.ingredient == ingredient)
    )
    association_query = (
        association_query
        .filter(IngredientsAssociation.ingredient == ingredient)
    )

if last_id:
    receipts_query = receipts_query.filter(Receipt.id >= last_id)
    association_query = association_query.filter(Receipt.id >= last_id)

if search:
    # lower() or upper() doesn't work with SQLite.
    association_query = (
        association_query.filter(
            or_(Receipt.title.like(f'%{search.lower()}%'),
                Receipt.title.like(f'%{search.title()}%'))
        )
    )
    receipts_query = (
        receipts_query.filter(
            or_(Receipt.title.like(f'%{search.lower()}%'),
                Receipt.title.like(f'%{search.title()}%'))
        )
    )

start_time = time.time()
receipts = receipts_query.limit(25).all()
print("receipts --- %s seconds ---" % (time.time() - start_time))
start_time = time.time()
ingredient_assoc = association_query.limit(25).all()
print("ingredients --- %s seconds ---" % (time.time() - start_time))

for receipt in receipts:
    print(receipt)

for receipt in ingredient_assoc:
    print(receipt.receipt)
