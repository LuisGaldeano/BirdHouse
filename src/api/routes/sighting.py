from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db

from models.sighting import Sighting

router = APIRouter()

# @app.get("/sighting")
# async def sighting():
#     last_sighting: Sighting | None = (
#         db_session.query(Sighting)
#         .filter_by(message_send=True)
#         .order_by(Sighting.id.desc())
#         .first()
#     )
#
#     message_send = False
#     if not last_sighting or not last_sighting.recently_sighting:
#         message_send = True
#         logger.info("Sending message with sighting")
#         await send_message(settings.TELEGRAM_SIGHTING_MESSAGE)
#
#     db_session.add(Sighting(message_send=message_send))
#     db_session.commit()
#
#     return {
#         "received": True,
#         "message_send": message_send,
#     }
