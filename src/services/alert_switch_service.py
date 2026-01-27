# -*- coding: utf-8 -*-
from repositories.alert_switch_repository import AlertSwitchRepository


class AlertSwitchService:
    def __init__(self, repo: AlertSwitchRepository):
        self.repo = repo

    def set_enabled(self, enabled: bool) -> dict:
        last_alert = self.repo.get_last()

        if last_alert and last_alert.enabled is enabled:
            return {
                "enabled": enabled,
                "created": False,
                "last_alert_id": last_alert.id,
            }

        new_event = self.repo.add(enabled)
        self.repo.db.commit()
        self.repo.db.refresh(new_event)

        return {
            "enabled": new_event.enabled,
            "created": True,
            "id": new_event.id,
            "created_at": new_event.created_at,
        }

    def get_status(self) -> dict:
        alert = self.repo.get_last()
        if alert is None:
            return {"error": "There are no records"}
        return {"alert_status": alert.enabled}
