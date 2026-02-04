# -*- coding: utf-8 -*-
import os
from datetime import datetime, timezone, timedelta

from repositories.alert_switch_repository import AlertSwitchRepository
from repositories.sighting_repository import SightingRepository
from settings.logging import get_logger
from settings.settings import env_vars
from messages.telegram import send_message, send_image

logger = get_logger(__name__)


class SightingService:
    def __init__(self, alert_repo: AlertSwitchRepository, sighting_repo: SightingRepository):
        self.alert_repo = alert_repo
        self.sighting_repo = sighting_repo

    def _waiting_time_seconds(self) -> float:
        return float(env_vars.RECENTLY_SIGHTING)

    def _assert_alerts_enabled(self) -> None:
        alert = self.alert_repo.get_last()
        if not (alert and alert.enabled):
            raise PermissionError("Alerts are not enabled")

    def _cooldown_passed(self, *, now: datetime, photo: bool) -> bool:
        waiting_time = self._waiting_time_seconds()
        last_sent = self.sighting_repo.get_last_sent_by_type(photo=photo)

        if last_sent is None:
            return True

        dt = last_sent.date
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        return dt <= now - timedelta(seconds=waiting_time)

    async def trigger_sighting_message(self) -> dict:
        now = datetime.now(timezone.utc)
        self._assert_alerts_enabled()

        should_send = self._cooldown_passed(now=now, photo=False)

        if should_send:
            logger.info("Sending message with sighting")
            message = f"{env_vars.TELEGRAM_SIGHTING_MESSAGE} - URL: {env_vars.CAMERA_URL}"
            await send_message(message)

        ev = self.sighting_repo.add(message_send=should_send, date=now, photo=False)
        self.sighting_repo.db.commit()
        self.sighting_repo.db.refresh(ev)

        return {"sent": should_send, "event_id": ev.id}

    async def trigger_sighting_photo(self) -> dict:
        now = datetime.now(timezone.utc)
        self._assert_alerts_enabled()

        should_send = self._cooldown_passed(now=now, photo=True)

        if should_send:
            logger.info("Sending photo with sighting")
            file = "last_sighting.jpg"
            image_path = os.path.join(env_vars.SIGHTING_PATH, file,)
            caption = f"{env_vars.TELEGRAM_SIGHTING_MESSAGE} - URL: {env_vars.CAMERA_URL}"
            await send_image(image_path=image_path, caption=caption)

        ev = self.sighting_repo.add(message_send=should_send, date=now, photo=True)
        self.sighting_repo.db.commit()
        self.sighting_repo.db.refresh(ev)

        return {"sent": should_send, "event_id": ev.id}
