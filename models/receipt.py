from sqlalchemy import Column, String, Integer, Text, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from . import Base
from .user import User
from .category import Category
from .tag import tags_association_table


class Receipt(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    title = Column(String(40), nullable=False)
    text = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    picture = Column(String(50), nullable=False)
    picture_min = Column(String(50), nullable=False)
    is_published = Column(Boolean, nullable=False, default=True)

    user = relationship('User', back_populates='receipts')
    comments = relationship('Comment', back_populates='receipt')

    tags = relationship('Tag', secondary=tags_association_table,
                        back_populates='receipts')
    # tags = relationship('TagsAssociation', back_populates='receipt')

    ingredients = relationship('IngredientsAssociation',
                               back_populates='receipt')
    category = relationship('Category', back_populates='receipts')

    @hybrid_property
    def lower_title(self):
        return func.lower(self.title)

    def __repr__(self):
        return f'<Receipt #{self.id} {self.user_id} {self.title}>'
