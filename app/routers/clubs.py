from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app import models, schemas
from app.deps import get_current_user, require_role

router = APIRouter()

@router.post("/", response_model=schemas.ClubOut)
def create_club(payload: schemas.ClubCreate, db: Session = Depends(get_db), user: models.User = Depends(require_role("admin","faculty","student"))):
    exists = db.query(models.Club).filter(models.Club.name == payload.name).first()
    if exists: raise HTTPException(400, detail="Club already exists")
    c = models.Club(name=payload.name, description=payload.description, owner_id=user.id)
    db.add(c); db.commit(); db.refresh(c)
    return c

@router.get("/", response_model=List[schemas.ClubOut])
def list_clubs(db: Session = Depends(get_db)):
    return db.query(models.Club).all()

@router.post("/{club_id}/join")
def request_join(club_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    c = db.query(models.Club).get(club_id)
    if not c: raise HTTPException(404, detail="Club not found")
    jr = models.ClubJoinRequest(club_id=club_id, user_id=user.id)
    db.add(jr); db.commit()
    return {"detail": "Join request submitted"}

@router.post("/{club_id}/join/{req_id}/approve")
def approve_join(club_id: int, req_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    jr = db.query(models.ClubJoinRequest).get(req_id)
    c = db.query(models.Club).get(club_id)
    if not jr or not c: raise HTTPException(404, detail="Not found")
    if c.owner_id != user.id and user.role != "admin":
        raise HTTPException(403, detail="Only club owner/admin can approve")
    jr.status = "approved"
    # add to members
    c.members.append(db.query(models.User).get(jr.user_id))
    db.commit()
    return {"detail": "Approved"}

@router.post("/{club_id}/posts", response_model=schemas.ClubPostOut)
def club_post(club_id: int, payload: schemas.ClubPostCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    c = db.query(models.Club).get(club_id)
    if not c: raise HTTPException(404, detail="Club not found")
    if user not in c.members and user.id != c.owner_id and user.role != "admin":
        raise HTTPException(403, detail="Join the club first")
    p = models.ClubPost(club_id=club_id, author_id=user.id, content=payload.content)
    db.add(p); db.commit(); db.refresh(p)
    return p

@router.get("/{club_id}/posts", response_model=List[schemas.ClubPostOut])
def list_posts(club_id: int, db: Session = Depends(get_db)):
    return db.query(models.ClubPost).filter(models.ClubPost.club_id == club_id).order_by(models.ClubPost.created_at.desc()).all()
