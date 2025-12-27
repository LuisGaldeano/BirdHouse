import os
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
