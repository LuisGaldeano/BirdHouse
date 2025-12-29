# -*- coding: utf-8 -*-
from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from settings.logging import get_logger
from settings.connection import SQLALCHEMY_DATABASE_URL

logger = get_logger(__name__)

Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, pool_size=5, max_overflow=10)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    logger.info('Initializing database (create_all)')
    Base.metadata.create_all(bind=engine)
    logger.info('Database initialized')


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
