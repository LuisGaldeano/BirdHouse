# -*- coding: utf-8 -*-
import os
from typing import Any, Dict, List

from pydantic.v1 import BaseSettings
from settings.settings import env_vars


class AppSettings(BaseSettings):
    app_env: str = env_vars.ENVIRONMENT
    debug: bool = False
    docs_url: str = '/docs'
    openapi_prefix: str = ''
    openapi_url: str = '/openapi.json'
    redoc_url: str = '/redoc'
    title: str = 'BirdHouse'
    description: str = 'API to manage the birdhouse'
    version: str = '1.0.0'

    allowed_hosts: List[str] = env_vars.ALLOWED_HOSTS.split()

    api_prefix: str = '/api'

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            'debug': self.debug,
            'docs_url': self.docs_url,
            'openapi_prefix': self.openapi_prefix,
            'openapi_url': self.openapi_url,
            'redoc_url': self.redoc_url,
            'title': self.title,
            'description': self.description,
            'version': self.version,
        }
