# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session
from models.alert import AlertSwitch


class AlertSwitchRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_last(self) -> AlertSwitch | None:
        return self.db.query(AlertSwitch).order_by(AlertSwitch.id.desc()).first()

    def add(self, enabled: bool) -> AlertSwitch:
        new_event = AlertSwitch(enabled=enabled)
        self.db.add(new_event)
        return new_event
