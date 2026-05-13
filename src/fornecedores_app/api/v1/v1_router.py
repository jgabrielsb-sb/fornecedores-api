from fastapi import APIRouter

from fornecedores_app.config import settings

from .controllers.fornecedor_controller import router as fornecedor_router
from .controllers.fornecedor_on_protheus_controller import router as fornecedor_on_protheus_router
from .controllers.fornecedor_to_update_controller import router as fornecedor_to_update_router
from .controllers.health_controller import router as health_router
from .controllers.municipio_controller import router as municipio_router

v1_router = APIRouter(prefix=f"{settings.API_PREFIX}/v1")

v1_router.include_router(health_router)
v1_router.include_router(fornecedor_router)
v1_router.include_router(fornecedor_on_protheus_router)
v1_router.include_router(fornecedor_to_update_router)
v1_router.include_router(municipio_router)
