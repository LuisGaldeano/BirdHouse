# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, DateTime, Boolean, func
from database.database import Base


class Light(Base):
    __tablename__ = 'light'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    light_status = Column(Boolean, nullable=False)

    def __str__(self):
        return f'{self.id} - {self.date} - {self.message_send}'
