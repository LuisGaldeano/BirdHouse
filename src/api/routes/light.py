from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db

from models.light import Light

router = APIRouter()


@router.post("/light/on")
def light_on(db: Session = Depends(get_db)):
    last = db.query(Light).order_by(Light.id.desc()).first()

    if last and last.light_status is True:
        return {"light_status": True, "created": False, "last_id": last.id}

    new_event = Light(light_status=True)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return {
        "light_status": new_event.light_status,
        "created": True,
        "id": new_event.id,
        "created_at": new_event.date,
    }


@router.post("/light/off")
def light_off(db: Session = Depends(get_db)):
    last = db.query(Light).order_by(Light.id.desc()).first()

    if last and last.light_status is False:
        return {"light_status": False, "created": False, "last_id": last.id}

    new_event = Light(light_status=False)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return {
        "light_status": new_event.light_status,
        "created": True,
        "id": new_event.id,
        "created_at": new_event.date,
    }


@router.get('/light_status')
async def light_status(db: Session = Depends(get_db)):
    sighting = db.query(Light).order_by(Light.id.desc()).first()

    if sighting is None:
        return {"error": "There are no records"}

    return {"light_status": sighting.light_status}
