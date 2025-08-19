from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app import models, schemas
from app.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.EventOut)
def create_event(payload: schemas.EventCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    e = models.Event(title=payload.title, description=payload.description, category=payload.category,
                     starts_at=payload.starts_at, ends_at=payload.ends_at, location=payload.location, created_by=user.id)
    db.add(e); db.commit(); db.refresh(e)
    return e

@router.get("/", response_model=List[schemas.EventOut])
def list_events(db: Session = Depends(get_db)):
    return db.query(models.Event).order_by(models.Event.starts_at.desc()).all()

@router.post("/{eid}/rsvp", response_model=schemas.RSVPOut)
def rsvp(eid: int, payload: schemas.RSVPCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    e = db.query(models.Event).get(eid)
    if not e: raise HTTPException(404, detail="Event not found")
    r = models.RSVP(event_id=eid, user_id=user.id, status=payload.status)
    db.add(r); db.commit(); db.refresh(r)
    return r

@router.get("/{eid}/rsvps", response_model=List[schemas.RSVPOut])
def list_rsvps(eid: int, db: Session = Depends(get_db)):
    return db.query(models.RSVP).filter(models.RSVP.event_id == eid).all()
