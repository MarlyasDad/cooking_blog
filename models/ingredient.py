from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import Base
from .receipt import Receipt


class Ingredient(Base):
    name = Column(String(30), nullable=False)

    receipts = relationship("IngredientsAssociation",
                            back_populates="ingredient")

    def __repr__(self):
        return f'<Ingredient #{self.id} {self.name}>'


class IngredientsAssociation(Base):
    receipt_id = Column(Integer, ForeignKey(Receipt.id))
    ingredient_id = Column(Integer, ForeignKey(Ingredient.id))

    quantity = Column(Integer, nullable=False)
    measure = Column(String(10), nullable=False)
    correction = Column(String(50), nullable=True)

    ingredient = relationship("Ingredient", back_populates="receipts")
    receipt = relationship("Receipt", back_populates="ingredients")
