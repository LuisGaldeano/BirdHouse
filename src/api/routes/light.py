# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from repositories.light_repository import LightRepository
from services.light_service import LightService

router = APIRouter()


def get_light_service(db: Session = Depends(get_db)) -> LightService:
    repo = LightRepository(db)
    return LightService(repo)


@router.post("/on")
def light_on(service: LightService = Depends(get_light_service)):
    return service.set_status(True)


@router.post("/off")
def light_off(service: LightService = Depends(get_light_service)):
    return service.set_status(False)


@router.get("/light_status")
def light_status(service: LightService = Depends(get_light_service)):
    return service.get_status()
