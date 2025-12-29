# -*- coding: utf-8 -*-
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Boolean, DateTime
from database.database import Base



class AlertSwitch(Base):
    __tablename__ = 'alert_switch'

    id = Column(Integer, primary_key=True, index=True)
    enabled = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    def __str__(self):
        return f'{self.id} - {self.created_at} - {self.enabled}'
