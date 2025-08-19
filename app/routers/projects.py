from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app import models, schemas
from app.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.ProjectOut)
def create_project(payload: schemas.ProjectCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    p = models.Project(title=payload.title, description=payload.description, github=payload.github, demo_url=payload.demo_url, owner_id=user.id)
    db.add(p); db.commit(); db.refresh(p)
    return p

@router.get("/", response_model=List[schemas.ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).order_by(models.Project.created_at.desc()).all()

@router.post("/{pid}/collaborators", response_model=schemas.CollaboratorRequestOut)
def request_collab(pid: int, payload: schemas.CollaboratorRequestCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    proj = db.query(models.Project).get(pid)
    if not proj: raise HTTPException(404, detail="Project not found")
    cr = models.CollaboratorRequest(project_id=pid, user_id=user.id, message=payload.message)
    db.add(cr); db.commit(); db.refresh(cr)
    return cr

@router.get("/{pid}/collaborators", response_model=List[schemas.CollaboratorRequestOut])
def list_collab_requests(pid: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return db.query(models.CollaboratorRequest).filter(models.CollaboratorRequest.project_id == pid).all()
