from fastapi import APIRouter

from fornecedores_app.core.config import settings

from .controllers.fornecedor_controller import router as fornecedor_router
from .controllers.health_controller import router as health_router

v1_router = APIRouter(prefix=f"{settings.API_PREFIX}/v1")

v1_router.include_router(health_router)
v1_router.include_router(fornecedor_router)
