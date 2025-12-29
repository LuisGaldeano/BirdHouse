# -*- coding: utf-8 -*-
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, Boolean
from database.database import Base


class Sighting(Base):
    __tablename__ = 'sighting'

    id = Column(Integer(), primary_key=True)
    date = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    message_send = Column(Boolean(), default=True)
    photo = Column(Boolean(), default=False)

    def __str__(self):
        return f'{self.id} - {self.date} - {self.message_send}'
