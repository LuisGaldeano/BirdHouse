# -*- coding: utf-8 -*-
import os
from settings.settings import env_vars

# Database parameters
db_host = env_vars.POSTGRES_HOST
db_user = env_vars.POSTGRES_USER
db_password = env_vars.POSTGRES_PASSWORD
db_database = env_vars.POSTGRES_DB
db_port = env_vars.POSTGRES_INTERNAL_PORT

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"
)
