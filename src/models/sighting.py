import settings
from datetime import datetime, timezone

from database.database import Base
from sqlalchemy import Column, Integer, DateTime, Boolean


class Sighting(Base):
    __tablename__ = 'sighting'
    id = Column(Integer(), primary_key=True)
    date = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    message_send = Column(Boolean(), default=True)

    def __str__(self):
        return f'{self.id} - {self.date} - {self.message_send}'

    @property
    def recently_sighting(self) -> bool:
        now = datetime.now(timezone.utc)
        dt = self.date

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        else:
            dt = dt.astimezone(timezone.utc)

        elapsed = (now - dt).total_seconds()
        return elapsed <= settings.RECENTLY_SIGHTING
