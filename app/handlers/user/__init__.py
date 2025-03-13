from .settings import router as settings_router
from .menu import router as menu_router
from .plan_maker import router as plan_maker_router
from .progress import router as progress_router


user_routers = [settings_router, menu_router, plan_maker_router, progress_router]

__all__ = [
    'user_routers'
]