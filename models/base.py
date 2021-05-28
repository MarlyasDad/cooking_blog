from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from config import CBLOG_SA_DB_URI

engine = create_engine(CBLOG_SA_DB_URI)


class Base:
    @declared_attr
    def __tablename__(self):
        return f'cblog_{self.__name__.lower()}'

    id = Column(Integer, primary_key=True, autoincrement=True)


Base = declarative_base(cls=Base, bind=engine)
