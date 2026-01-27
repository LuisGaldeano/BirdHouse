# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session
from models.sighting import Sighting

class SightingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_last_sent_by_type(self, *, photo: bool) -> Sighting | None:
        return (
            self.db.query(Sighting)
            .filter_by(message_send=True, photo=photo)
            .order_by(Sighting.id.desc())
            .first()
        )

    def add(self, *, message_send: bool, date, photo: bool) -> Sighting:
        sighting = Sighting(message_send=message_send, date=date, photo=photo)
        self.db.add(sighting)
        return sighting
