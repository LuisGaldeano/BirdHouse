# -*- coding: utf-8 -*-
import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settings:
    PROJECT_NAME: str
    ENVIRONMENT: str
    LOG_LEVEL: str

    FASTAPI_HOST: str
    FASTAPI_PORT: str

    ALLOW_CREDENTIALS: str
    ALLOW_METHODS: str
    ALLOW_HEADERS: str
    ALLOWED_HOSTS: str

    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_EXTERNAL_PORT: str
    POSTGRES_INTERNAL_PORT: str

    TELEGRAM_SIGHTING_MESSAGE: str
    TELEGRAM_TOKEN: str
    TELEGRAM_CHAT_ID: str

    RECENTLY_SIGHTING: str
    SIGHTING_PATH: str

    CAMERA_URL: str


def load_settings() -> Settings:
    return Settings(
        PROJECT_NAME=os.getenv("PROJECT_NAME", default="birdhouse"),
        ENVIRONMENT=os.getenv("ENVIRONMENT", default="dev"),
        LOG_LEVEL=os.getenv("LOG_LEVEL", default="INFO"),

        FASTAPI_HOST=os.getenv("FASTAPI_HOST", default="0.0.0.0"),
        FASTAPI_PORT=os.getenv("FASTAPI_PORT", default="8000"),

        ALLOW_CREDENTIALS=os.getenv("ALLOW_CREDENTIALS", default=True),
        ALLOW_METHODS=os.getenv("ALLOW_METHODS", default="['*']"),
        ALLOW_HEADERS=os.getenv("ALLOW_HEADERS", default="['*']"),
        ALLOWED_HOSTS=os.getenv("ALLOW_HOSTS", default="['*']"),

        POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD"),
        POSTGRES_HOST=os.getenv("POSTGRES_HOST", default="postgres"),
        POSTGRES_USER=os.getenv("POSTGRES_USER", default="postgres"),
        POSTGRES_DB=os.getenv("POSTGRES_DB", default="birdhouse"),
        POSTGRES_EXTERNAL_PORT=os.getenv("POSTGRES_EXTERNAL_PORT", default="1900"),
        POSTGRES_INTERNAL_PORT=os.getenv("POSTGRES_INTERNAL_PORT", default="5432"),

        TELEGRAM_SIGHTING_MESSAGE=os.getenv("TELEGRAM_SIGHTING_MESSAGE", default="There is movement in the nest!"),
        TELEGRAM_TOKEN=os.getenv("TELEGRAM_TOKEN"),
        TELEGRAM_CHAT_ID=os.getenv("TELEGRAM_CHAT_ID"),

        RECENTLY_SIGHTING=os.getenv("RECENTLY_SIGHTING", default="60"),
        SIGHTING_PATH=os.getenv("SIGHTING_PATH", default="/src/media"),

        CAMERA_URL=os.getenv("CAMERA_URL", default=""),
    )


env_vars = load_settings()
