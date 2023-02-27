from sanic import Blueprint
from .user import user_bp, admin_user_bp

bg_tuple = (
    user_bp,
    admin_user_bp
)

bg_group = Blueprint.group(
    *bg_tuple,
    url_prefix='/api'
)

__all__ = [
    'bg_group'
]