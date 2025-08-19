from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app import models, schemas
from app.deps import get_current_user, require_role

router = APIRouter()

@router.post("/", response_model=schemas.PlacementOut)
def post_listing(payload: schemas.PlacementCreate, db: Session = Depends(get_db), user: models.User = Depends(require_role("admin","faculty"))):
    p = models.PlacementListing(company=payload.company, role=payload.role, description=payload.description, posted_by=user.id, deadline=payload.deadline)
    db.add(p); db.commit(); db.refresh(p)
    return p

@router.get("/", response_model=List[schemas.PlacementOut])
def list_listings(db: Session = Depends(get_db)):
    return db.query(models.PlacementListing).order_by(models.PlacementListing.deadline.asc()).all()

@router.post("/experiences", response_model=schemas.AlumniExperienceOut)
def add_experience(payload: schemas.AlumniExperienceCreate, db: Session = Depends(get_db), user: models.User = Depends(require_role("alumni","admin"))):
    exp = models.AlumniExperience(alumni_id=user.id, company=payload.company, content=payload.content)
    db.add(exp); db.commit(); db.refresh(exp)
    return exp

@router.get("/experiences", response_model=List[schemas.AlumniExperienceOut])
def list_experiences(db: Session = Depends(get_db)):
    return db.query(models.AlumniExperience).order_by(models.AlumniExperience.created_at.desc()).all()
