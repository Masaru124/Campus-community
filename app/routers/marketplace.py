from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app import models, schemas
from app.deps import get_current_user

router = APIRouter()

@router.post("/listings", response_model=schemas.ListingOut)
def create_listing(payload: schemas.ListingCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    l = models.Listing(title=payload.title, description=payload.description, price=payload.price, category=payload.category, owner_id=user.id)
    db.add(l); db.commit(); db.refresh(l)
    return l

@router.get("/listings", response_model=List[schemas.ListingOut])
def list_listings(db: Session = Depends(get_db)):
    return db.query(models.Listing).order_by(models.Listing.created_at.desc()).all()

@router.post("/listings/{lid}/message", response_model=schemas.MessageOut)
def send_message(lid: int, payload: schemas.MessageCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    listing = db.query(models.Listing).get(lid)
    if not listing: raise HTTPException(404, detail="Listing not found")
    msg = models.ListingMessage(listing_id=lid, sender_id=user.id, receiver_id=payload.receiver_id, content=payload.content)
    db.add(msg); db.commit(); db.refresh(msg)
    return msg

@router.get("/listings/{lid}/messages", response_model=List[schemas.MessageOut])
def get_messages(lid: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return db.query(models.ListingMessage).filter(models.ListingMessage.listing_id == lid).order_by(models.ListingMessage.created_at.asc()).all()
