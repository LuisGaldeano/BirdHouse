from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from database.database import init_db
from api.routes.api import router as api_router
from settings.config import get_app_settings
from settings.logging import logger


def get_application(db_initialization: bool = True) -> FastAPI:
    settings = get_app_settings()
    logger.info("Legaly is in '%s' environment", settings.app_env)

    # Load app
    application = FastAPI(**settings.fastapi_kwargs)

    if db_initialization:
        # Init the database
        init_db()

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(api_router, prefix=settings.api_prefix)

    return application