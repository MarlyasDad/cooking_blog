from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from . import Base, Receipt, User


class Comment(Base):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    text = Column(Text, nullable=False)
    created = Column(DateTime, default=datetime.now)

    user = relationship('User', back_populates='comments')
    receipt = relationship('Receipt', back_populates='comments')

    def __repr__(self):
        return f'<Comment #{self.user_id} {self.receipt_id}>'
