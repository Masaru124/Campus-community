from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app import models, schemas
from app.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.HackathonOut)
def create_hackathon(payload: schemas.HackathonCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    h = models.Hackathon(name=payload.name, description=payload.description, starts_at=payload.starts_at, ends_at=payload.ends_at)
    db.add(h); db.commit(); db.refresh(h)
    return h

@router.get("/", response_model=List[schemas.HackathonOut])
def list_hackathons(db: Session = Depends(get_db)):
    return db.query(models.Hackathon).order_by(models.Hackathon.starts_at.desc()).all()

@router.post("/{hid}/teams", response_model=schemas.TeamOut)
def create_team(hid: int, payload: schemas.TeamCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    h = db.query(models.Hackathon).get(hid)
    if not h: raise HTTPException(404, detail="Hackathon not found")
    t = models.HackathonTeam(hackathon_id=hid, name=payload.name)
    db.add(t); db.commit(); db.refresh(t)
    return t

@router.post("/{hid}/leaderboard", response_model=schemas.LeaderboardOut)
def set_score(hid: int, payload: schemas.LeaderboardUpdate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    h = db.query(models.Hackathon).get(hid)
    if not h: raise HTTPException(404, detail="Hackathon not found")
    lb = models.LeaderboardEntry(hackathon_id=hid, team_id=payload.team_id, score=payload.score)
    db.add(lb); db.commit(); db.refresh(lb)
    return lb

@router.get("/{hid}/leaderboard", response_model=List[schemas.LeaderboardOut])
def get_leaderboard(hid: int, db: Session = Depends(get_db)):
    return db.query(models.LeaderboardEntry).filter(models.LeaderboardEntry.hackathon_id == hid).order_by(models.LeaderboardEntry.score.desc()).all()
