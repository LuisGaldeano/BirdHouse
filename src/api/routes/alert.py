# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from repositories.alert_switch_repository import AlertSwitchRepository
from services.alert_switch_service import AlertSwitchService

router = APIRouter()


def get_alert_switch_service(db: Session = Depends(get_db)) -> AlertSwitchService:
    repo = AlertSwitchRepository(db)
    return AlertSwitchService(repo)


@router.post("/on")
def alert_switch_on(service: AlertSwitchService = Depends(get_alert_switch_service)):
    return service.set_enabled(True)


@router.post("/off")
def alert_switch_off(service: AlertSwitchService = Depends(get_alert_switch_service)):
    return service.set_enabled(False)


@router.get("/alert_status")
def alert_status(service: AlertSwitchService = Depends(get_alert_switch_service)):
    return service.get_status()
