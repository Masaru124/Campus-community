from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import engine, Base
from app.config import settings
from app.routers import users, notices, clubs, forum, projects, events, placements, marketplace, alumni, lostfound, utilities, hackathons, moderation
import os

# Create tables
Base.metadata.create_all(bind=engine)

# Ensure upload dir exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="Campus Platform Backend (Except Study Section)", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/auth", tags=["Auth & Users"])
app.include_router(notices.router, prefix="/notices", tags=["Notices"])
app.include_router(clubs.router, prefix="/clubs", tags=["Clubs"])
app.include_router(forum.router, prefix="/forum", tags=["Forum"])
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(events.router, prefix="/events", tags=["Events"])
app.include_router(placements.router, prefix="/placements", tags=["Placements"])
app.include_router(marketplace.router, prefix="/marketplace", tags=["Marketplace"])
app.include_router(alumni.router, prefix="/alumni", tags=["Alumni & Mentorship"])
app.include_router(lostfound.router, prefix="/lostfound", tags=["Lost & Found"])
app.include_router(utilities.router, prefix="/utilities", tags=["Utilities"])
app.include_router(hackathons.router, prefix="/hackathons", tags=["Hackathons"])
app.include_router(moderation.router, prefix="/moderation", tags=["Moderation"])

@app.get("/", tags=["Health"])
def root():
    return {"status": "ok"}
