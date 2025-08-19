from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app import models, schemas
from app.deps import get_current_user, require_role

router = APIRouter()

@router.post("/reports", response_model=schemas.ReportOut)
def report(payload: schemas.ReportCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    r = models.Report(reporter_id=user.id, target_type=payload.target_type, target_id=payload.target_id, reason=payload.reason)
    db.add(r); db.commit(); db.refresh(r)
    return r

@router.get("/reports", response_model=List[schemas.ReportOut])
def list_reports(db: Session = Depends(get_db), user: models.User = Depends(require_role("admin"))):
    return db.query(models.Report).order_by(models.Report.created_at.desc()).all()

@router.post("/reports/{rid}/close", response_model=schemas.ReportOut)
def close_report(rid: int, db: Session = Depends(get_db), user: models.User = Depends(require_role("admin"))):
    r = db.query(models.Report).get(rid)
    if not r: raise HTTPException(404, detail="Not found")
    r.status = "closed"; db.commit(); db.refresh(r); return r
