from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app import models, schemas
from app.deps import get_current_user, require_role

router = APIRouter()

@router.post("/", response_model=schemas.NoticeOut)
def create_notice(payload: schemas.NoticeCreate, db: Session = Depends(get_db), user: models.User = Depends(require_role("admin","faculty"))):
    n = models.Notice(title=payload.title, content=payload.content, audience=payload.audience, author_id=user.id)
    db.add(n); db.commit(); db.refresh(n)
    return n

@router.get("/", response_model=List[schemas.NoticeOut])
def list_notices(db: Session = Depends(get_db)):
    return db.query(models.Notice).order_by(models.Notice.created_at.desc()).all()
