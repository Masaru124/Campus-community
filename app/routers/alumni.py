from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app import models, schemas
from app.deps import get_current_user, require_role

router = APIRouter()

@router.post("/mentorships", response_model=schemas.MentorshipOut)
def create_mentorship(payload: schemas.MentorshipCreate, db: Session = Depends(get_db), mentor: models.User = Depends(require_role("alumni","admin"))):
    m = models.Mentorship(mentor_id=mentor.id, mentee_id=payload.mentee_id, topic=payload.topic)
    db.add(m); db.commit(); db.refresh(m)
    return m

@router.get("/mentorships", response_model=List[schemas.MentorshipOut])
def list_mentorships(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    # show those related to user
    return db.query(models.Mentorship).filter((models.Mentorship.mentor_id == user.id) | (models.Mentorship.mentee_id == user.id)).all()

@router.post("/mentorships/{mid}/accept", response_model=schemas.MentorshipOut)
def accept_mentorship(mid: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    m = db.query(models.Mentorship).get(mid)
    if not m: raise HTTPException(404, detail="Not found")
    if m.mentor_id != user.id and user.role != "admin":
        raise HTTPException(403, detail="Only mentor/admin can accept")
    m.status = "accepted"; db.commit(); db.refresh(m); return m
