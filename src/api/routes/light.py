import os

from fastapi import APIRouter
from crud.cat_scope_workplace_rel import CatScopeWorkplaceRelRepository
from models.schema.cat_scope_workplace_rel import NewCatScopeWorkplaceRel
from database.database import db_dependency
from resources import responses
from settings.logging import logger
from database.database import db_session

router = APIRouter()

@router.get("/cat_scope_workplace_rel/{workplace_id}")
async def cat_scope_workplace_rel_by_workplace_id(db: db_dependency, workplace_id: int):
    data = CatScopeWorkplaceRelRepository(db=db).get_by_int_field(field_id=workplace_id)
    return responses.ApiResponse(data=data).generate_response()


@router.post("/light/on")
async def light_on():

    light = db_session.query(Sighting)
        .filter_by(message_send=True)
        .order_by(Sighting.id.desc())
        .first()
    )
    if light:
        return {"light_active": light}




    logger.info("Light set to True")



@app.post("/light/off")
async def light_off():
    settings.LIGHT_ACTIVE = False
    logger.info("Light set to False")
    return {"light_active": settings.LIGHT_ACTIVE}


@app.get('/light_value')
async def light_value():
    return settings.LIGHT_ACTIVE
