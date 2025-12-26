from fastapi import APIRouter

from api.routes import light

router = APIRouter()

router.include_router(light.router, tags=["light"], prefix="/light")