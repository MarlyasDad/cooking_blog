from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from . import Base


class Category(Base):
    name = Column(String(50), nullable=False, unique=True)
    alias = Column(String(50), nullable=False, unique=True)

    receipts = relationship('Receipt', back_populates='category')
