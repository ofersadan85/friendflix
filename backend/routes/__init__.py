from .auth import router as auth_router
from .healthcheck import router as healthcheck_router

all_routers = [auth_router, healthcheck_router]
