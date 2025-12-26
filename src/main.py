import logging
import uvicorn
import settings

from database.database import init_db, Sighting, db_session
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from messages.telegram import send_message

logger = logging.getLogger(__name__)
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    logger.info('Starting bird house')
    # Start database
    init_db()
    logger.info('Bird house started')


@app.get('/ping')
async def root():
    logger.info('Ping ok')
    return 'Ok'


@app.get("/sighting")
async def sighting():
    last_sighting: Sighting | None = (
        db_session.query(Sighting)
        .filter_by(message_send=True)
        .order_by(Sighting.id.desc())
        .first()
    )

    message_send = False
    if not last_sighting or not last_sighting.recently_sighting:
        message_send = True
        logger.info("Sending message with sighting")
        await send_message(settings.TELEGRAM_SIGHTING_MESSAGE)

    db_session.add(Sighting(message_send=message_send))
    db_session.commit()

    return {
        "received": True,
        "message_send": message_send,
    }


@app.post("/light/on")
async def light_on():
    settings.LIGHT_ACTIVE = True
    logger.info("Light set to True")
    return {"light_active": settings.LIGHT_ACTIVE}


@app.post("/light/off")
async def light_off():
    settings.LIGHT_ACTIVE = False
    logger.info("Light set to False")
    return {"light_active": settings.LIGHT_ACTIVE}


@app.get('/light_value')
async def light_value():
    return settings.LIGHT_ACTIVE


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level=settings.LOG_LEVEL)
