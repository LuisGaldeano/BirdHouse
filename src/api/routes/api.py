# -*- coding: utf-8 -*-
from fastapi import APIRouter

from api.routes import light, sighting, alert

router = APIRouter()

router.include_router(light.router, tags=['light'], prefix='/light')
router.include_router(sighting.router, tags=['sighting'], prefix='/sighting')
router.include_router(alert.router, tags=['alert'], prefix='/alert')
