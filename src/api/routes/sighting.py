# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from database.database import get_db
from repositories.alert_switch_repository import AlertSwitchRepository
from repositories.sighting_repository import SightingRepository
from services.sighting_service import SightingService

router = APIRouter()


def get_sighting_service(db: Session = Depends(get_db)) -> SightingService:
    alert_repo = AlertSwitchRepository(db)
    sighting_repo = SightingRepository(db)
    return SightingService(alert_repo=alert_repo, sighting_repo=sighting_repo)


@router.post("/send_message")
async def send_message(
    response: Response,
    service: SightingService = Depends(get_sighting_service),
):
    try:
        result = await service.trigger_sighting_message()
    except PermissionError:
        response.status_code = status.HTTP_409_CONFLICT
        return {"error": "Alerts are not enabled"}

    if result["sent"]:
        response.status_code = status.HTTP_202_ACCEPTED
        return {"received": True, "sent": True, "event_id": result["event_id"]}

    response.status_code = status.HTTP_204_NO_CONTENT
    return None


@router.post("/send_photo")
async def send_photo(
    response: Response,
    service: SightingService = Depends(get_sighting_service),
):
    try:
        result = await service.trigger_sighting_photo()
    except PermissionError:
        response.status_code = status.HTTP_409_CONFLICT
        return {"error": "Alerts are not enabled"}

    if result["sent"]:
        response.status_code = status.HTTP_202_ACCEPTED
        return {"received": True, "sent": True, "event_id": result["event_id"]}

    response.status_code = status.HTTP_204_NO_CONTENT
    return None
