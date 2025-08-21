from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from app.db import get_db
from app import models, schemas
from app.auth import hash_password, verify_password, create_access_token
from app.deps import get_current_user
import re, os, shutil, secrets

router = APIRouter()
email_codes = {}  # demo store: {email: code}

@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    u = models.User(
        name=user.name, email=user.email, hashed_password=hash_password(user.password),
        role=user.role, branch=user.branch, year=user.year, achievements=user.achievements,
        linkedin=user.linkedin, github=user.github
    )
    db.add(u); db.commit(); db.refresh(u)
    # generate verification code (demo)
    code = secrets.token_hex(3)
    email_codes[user.email] = code
    print(f"[DEV] Verification code for {user.email}: {code}")
    return u

@router.post("/verify", response_model=schemas.UserOut)
def verify(req: schemas.EmailVerificationRequest, db: Session = Depends(get_db)):
    code = email_codes.get(req.email)
    if not code or code != req.code:
        raise HTTPException(400, detail="Invalid code")
    user = db.query(models.User).filter(models.User.email == req.email).first()
    if not user:
        raise HTTPException(404, detail="User not found")
    user.email_verified = True
    db.commit(); db.refresh(user)
    return user

@router.post("/login", response_model=schemas.Token)
def login(req: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == req.email).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserOut)
def me(current: models.User = Depends(get_current_user)):
    return current

@router.put("/me", response_model=schemas.UserOut)
def update_me(
    name: Optional[str] = Form(None),
    branch: Optional[str] = Form(None),
    year: Optional[int] = Form(None),
    achievements: Optional[str] = Form(None),
    linkedin: Optional[str] = Form(None),
    github: Optional[str] = Form(None),
    avatar: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current: models.User = Depends(get_current_user)
):
    if name is not None: current.name = name
    if branch is not None: current.branch = branch
    if year is not None: current.year = year
    if achievements is not None: current.achievements = achievements
    if linkedin is not None: current.linkedin = linkedin
    if github is not None: current.github = github
    # Save avatar if uploaded
    if avatar:
        filename = f"user_{current.id}_avatar_{secrets.token_hex(4)}_{avatar.filename}"
        path = os.path.join(settings.UPLOAD_DIR, filename)
        with open(path, "wb") as f:
            shutil.copyfileobj(avatar.file, f)
    db.commit(); db.refresh(current)
    return current
