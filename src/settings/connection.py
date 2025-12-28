import os

# Database parameters
db_host = os.getenv("POSTGRES_HOST", 'postgres')
db_user = os.getenv("POSTGRES_USER", 'postgres')
db_password = os.getenv("POSTGRES_PASSWORD", 'patata123')
db_database = os.getenv("POSTGRES_DB", 'birdhouse')
db_port = os.getenv("POSTGRES_INTERNAL_PORT", '1900')

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"
)