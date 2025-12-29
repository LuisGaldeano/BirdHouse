# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from models.alert import AlertSwitch

router = APIRouter()


@router.post('/on')
def alert_switch_on(db: Session = Depends(get_db)):
    last_alert = db.query(AlertSwitch).order_by(AlertSwitch.id.desc()).first()

    if last_alert and last_alert.enabled is True:
        return {'enabled': True, 'created': False, 'last_alert_id': last_alert.id}

    new_event = AlertSwitch(enabled=True)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return {
        'enabled': new_event.enabled,
        'created': True,
        'id': new_event.id,
        'created_at': new_event.created_at,
    }


@router.post('/off')
def alert_switch_off(db: Session = Depends(get_db)):
    last_alert = db.query(AlertSwitch).order_by(AlertSwitch.id.desc()).first()

    if last_alert and last_alert.enabled is False:
        return {'enabled': False, 'created': False, 'last_alert_id': last_alert.id}

    new_event = AlertSwitch(enabled=False)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return {
        'enabled': new_event.enabled,
        'created': True,
        'id': new_event.id,
        'created_at': new_event.created_at,
    }

@router.get('/alert_status')
async def alert_status(db: Session = Depends(get_db)):
    alert = db.query(AlertSwitch).order_by(AlertSwitch.id.desc()).first()

    if alert is None:
        return {'error': 'There are no records'}

    return {'alert_status': alert.enabled}
