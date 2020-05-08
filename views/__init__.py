from .auth import auth_app
from .user import users_app
from .receipt import receipts_app
from .comment import comments_app

__all__ = [
    'auth_app',
    'users_app',
    'receipts_app',
    'comments_app',
]
