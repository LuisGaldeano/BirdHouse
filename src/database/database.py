import settings
import logging
from datetime import datetime, timezone

from sqlalchemy import create_engine, Column, Integer, DateTime, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


logger = logging.getLogger(__name__)

engine = create_engine('sqlite:///database/birdHouse.db')
db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)


def init_db():
    logger.info('Initializing database')
    Model.metadata.create_all(bind=engine)
    logger.info('Database initialized')


Model = declarative_base(name='Model')
Model.query = db_session.query_property()


class Sighting(Model):
    __tablename__ = 'sighting'
    id = Column(Integer(), primary_key=True)
    date = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    message_send = Column(Boolean(), default=True)

    def __str__(self):
        return f'{self.id} - {self.date} - {self.message_send}'

    @property
    def recently_sighting(self):
        if settings.RECENTLY_SIGHTING < (datetime.now(timezone.utc).replace(tzinfo=None) - self.date).total_seconds():
            return False
        return True
