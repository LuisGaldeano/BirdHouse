# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session
from models.light import Light


class LightRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_last(self) -> Light | None:
        return self.db.query(Light).order_by(Light.id.desc()).first()

    def add(self, light_status: bool) -> Light:
        light = Light(light_status=light_status)
        self.db.add(light)
        return light
