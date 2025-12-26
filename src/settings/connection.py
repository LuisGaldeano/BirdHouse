import os

# Database parameters
db_host = os.getenv("POSTGRES_HOST")
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_database = os.getenv("POSTGRES_DB")
db_port = os.getenv("POSTGRES_INTERNAL_PORT")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"
)