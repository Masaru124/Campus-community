from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app import models, schemas
from app.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.LostFoundOut)
def post_item(payload: schemas.LostFoundCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    lf = models.LostFound(type=payload.type, title=payload.title, description=payload.description, contact=payload.contact, user_id=user.id)
    db.add(lf); db.commit(); db.refresh(lf)
    return lf

@router.get("/", response_model=List[schemas.LostFoundOut])
def list_items(db: Session = Depends(get_db)):
    return db.query(models.LostFound).order_by(models.LostFound.created_at.desc()).all()
