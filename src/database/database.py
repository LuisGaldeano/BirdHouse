import settings
import logging
from datetime import datetime, timezone
from typing import Annotated

from sqlalchemy import create_engine, Column, Integer, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends
from sqlalchemy.ext.declarative import declarative_base


logger = logging.getLogger(__name__)


DATABASE_URL = "sqlite:///./database/birdHouse.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # importante para SQLite en FastAPI
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db() -> None:
    logger.info("Initializing database")
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized")


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]



