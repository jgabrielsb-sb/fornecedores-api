import json
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from fornecedores_app.api.v1 import v1_router
from fornecedores_app.api.v1.models import dto_responses
from fornecedores_app.api.v1.services.exceptions import (
    ConflictException,
    ForbiddenException,
    InvalidFileException,
    NotFoundException,
)
from fornecedores_app.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title="Fornecedores API",
        version=settings.API_VERSION,
        docs_url=f"{settings.API_PREFIX}/docs",
        redoc_url=f"{settings.API_PREFIX}/redoc",
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
    )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content=dto_responses.Error422Response(
                message="Invalid request body or parameters: " + str(exc.errors()),
                path=request.url.path,
                timestamp=datetime.now().isoformat(),
            ).model_dump(mode="json"),
        )

    @app.exception_handler(NotFoundException)
    async def not_found_exception_handler(request: Request, exc: NotFoundException):
        return JSONResponse(
            status_code=404,
            content=dto_responses.Error404Response(
                message=str(exc),
                path=str(request.url),
                timestamp=datetime.now().isoformat(),
            ).model_dump(mode="json"),
        )

    @app.exception_handler(ConflictException)
    async def conflict_exception_handler(request: Request, exc: ConflictException):
        return JSONResponse(
            status_code=409,
            content=dto_responses.Error409Response(
                message=str(exc),
                path=str(request.url),
                timestamp=datetime.now().isoformat(),
            ).model_dump(mode="json"),
        )

    @app.exception_handler(ForbiddenException)
    async def forbidden_exception_handler(request: Request, exc: ForbiddenException):
        return JSONResponse(
            status_code=403,
            content=dto_responses.Error403Response(
                message=str(exc),
                path=str(request.url),
                timestamp=datetime.now().isoformat(),
            ).model_dump(mode="json"),
        )

    @app.exception_handler(InvalidFileException)
    async def invalid_file_exception_handler(request: Request, exc: InvalidFileException):
        return JSONResponse(
            status_code=400,
            content=dto_responses.Error400Response(
                message=str(exc),
                path=str(request.url),
                timestamp=datetime.now().isoformat(),
            ).model_dump(mode="json"),
        )

    app.openapi_tags = [
        {
            "name": "v1/health",
            "description": "Health and readiness endpoints (API v1)",
        },
        {
            "name": "v1/fornecedores",
            "description": "Fornecedor management endpoints (API v1)",
        },
        {
            "name": "v1/fornecedores-on-protheus",
            "description": "Fornecedor on Protheus management endpoints (API v1)",
        },
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(v1_router)
    return app
