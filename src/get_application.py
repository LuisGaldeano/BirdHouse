# -*- coding: utf-8 -*-
from fastapi import FastAPI

from database.database import init_db
from api.routes.api import router as api_router
from settings.config import get_app_settings
from settings.logging import get_logger

logger = get_logger(__name__)


def get_application(db_initialization: bool = True) -> FastAPI:
    settings = get_app_settings()
    logger.info("Legaly is in '%s' environment", settings.app_env)

    # Load app
    application = FastAPI(**settings.fastapi_kwargs)

    if db_initialization:
        # Init the database
        init_db()

    application.include_router(api_router, prefix=settings.api_prefix)

    return application
