from .settings import router as settings_router
from .menu import router as menu_router

user_routers = [settings_router, menu_router]

__all__ = [
    'user_routers'
]