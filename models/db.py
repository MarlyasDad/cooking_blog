from sqlalchemy.orm import sessionmaker, scoped_session
# from sqlalchemy.orm import joinedload
from .base import engine

session_factory = sessionmaker(bind=engine, autoflush=False)
Session = scoped_session(session_factory)
