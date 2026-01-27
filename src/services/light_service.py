# -*- coding: utf-8 -*-
from repositories.light_repository import LightRepository


class LightService:
    def __init__(self, repo: LightRepository):
        self.repo = repo

    def set_status(self, light_status: bool) -> dict:
        last = self.repo.get_last()

        if last and last.light_status is light_status:
            return {
                "light_status": light_status,
                "created": False,
                "last_id": last.id,
            }

        new_event = self.repo.add(light_status)
        self.repo.db.commit()
        self.repo.db.refresh(new_event)

        return {
            "light_status": new_event.light_status,
            "created": True,
            "id": new_event.id,
            "created_at": new_event.date,
        }

    def get_status(self) -> dict:
        last = self.repo.get_last()
        if last is None:
            return {"error": "There are no records"}
        return {"light_status": last.light_status}
