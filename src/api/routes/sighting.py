import os
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from models.alert import AlertSwitch
from settings.logging import get_logger
from messages.telegram import send_message
from models.sighting import Sighting

logger = get_logger(__name__)

router = APIRouter()

@router.get("/sighting")
async def sighting(db: Session = Depends(get_db)):
    waiting_time = float(os.getenv("RECENTLY_SIGHTING", "300"))
    now = datetime.now(timezone.utc)

    alert = db.query(AlertSwitch).order_by(AlertSwitch.id.desc()).first()

    if not alert.enabled:
        return {"Alerts are not enabled"}

    last_sighting = db.query(Sighting).filter_by(message_send=True).order_by(Sighting.id.desc()).first()

    message_send = False

    if last_sighting is None:
        message_send = True
    else:
        dt = last_sighting.date

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        if dt <= now - timedelta(seconds=waiting_time):
            message_send = True

    if message_send:
        logger.info("Sending message with sighting")
        message = f"{os.getenv('TELEGRAM_SIGHTING_MESSAGE')} - URL: {os.getenv('CAMERA_URL')}"
        await send_message(message)

    message = Sighting(message_send=message_send, date=now)
    db.add(message)
    db.commit()
    db.refresh(message)

    return {
        "received": True,
        "message_send": message_send,
    }