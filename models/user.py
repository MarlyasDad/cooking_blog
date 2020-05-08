import hashlib
from typing import Optional
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from . import Base


class User(Base, UserMixin):
    email = Column(String(50), nullable=False, unique=True)
    username = Column(String(30), nullable=False, unique=False)
    _password = Column("password", String(32), nullable=False)
    preferences = Column(Text, nullable=True)
    avatar = Column(String(100), nullable=True, unique=False,
                    default='default-min.png')

    receipts = relationship('Receipt', back_populates='user')
    comments = relationship('Comment', back_populates='user')

    def __init__(self, email: str, username: str, password: str,
                 preferences: Optional[str] = None,
                 avatar: Optional[str] = None):
        self.email = email
        self.username = username
        self.password = password
        self.preferences = preferences
        self.avatar = avatar

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value: str):
        self._password = self.hash_password(value)

    @classmethod
    def hash_password(cls, value: str) -> str:
        """
        Hashes the password
        :param value:
        :return:
        """
        return hashlib.md5(value.encode("utf-8")).hexdigest()

    def __repr__(self):
        return f'<User #{self.id} {self.username}>'
