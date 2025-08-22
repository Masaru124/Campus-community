from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
import datetime

# ---------- Auth & Users ----------
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str = "student"
    branch: str = ""
    year: int = 0
    achievements: str = ""
    linkedin: str = ""
    github: str = ""

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    email_verified: bool
    created_at: datetime.datetime
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class EmailVerificationRequest(BaseModel):
    email: EmailStr
    code: str

# ---------- Generic ----------
class IDOut(BaseModel):
    id: int

# ---------- Notices ----------
class NoticeCreate(BaseModel):
    title: str
    content: str
    audience: str = "all"

class NoticeOut(NoticeCreate):
    id: int
    author_id: int
    created_at: datetime.datetime
    class Config:
        from_attributes = True

# ---------- Clubs ----------
class ClubCreate(BaseModel):
    name: str
    description: str = ""

class ClubOut(ClubCreate):
    id: int
    owner_id: int
    class Config:
        from_attributes = True

class ClubPostCreate(BaseModel):
    content: str

class ClubPostOut(ClubPostCreate):
    id: int
    club_id: int
    author_id: int
    created_at: datetime.datetime
    class Config:
        from_attributes = True

# ---------- Forum ----------
class PostCreate(BaseModel):
    title: str
    content: str

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    created_at: datetime.datetime
    upvotes: int
    class Config:
        from_attributes = True

class QuestionCreate(BaseModel):
    title: str
    body: str
    tags: List[str] = []

class QuestionOut(BaseModel):
    id: int
    title: str
    body: str
    tags: List[str]
    author_id: int
    created_at: datetime.datetime
    upvotes: int
    class Config:
        from_attributes = True

class AnswerCreate(BaseModel):
    body: str

class AnswerOut(BaseModel):
    id: int
    question_id: int
    body: str
    author_id: int
    created_at: datetime.datetime
    upvotes: int
    class Config:
        from_attributes = True

# ---------- Projects ----------
class ProjectCreate(BaseModel):
    title: str
    description: str
    github: str = ""
    demo_url: str = ""

class ProjectOut(ProjectCreate):
    id: int
    owner_id: int
    created_at: datetime.datetime
    class Config:
        from_attributes = True

class CollaboratorRequestCreate(BaseModel):
    message: str = ""

class CollaboratorRequestOut(BaseModel):
    id: int
    project_id: int
    user_id: int
    message: str
    status: str
    class Config:
        from_attributes = True

# ---------- Events ----------
class EventCreate(BaseModel):
    title: str
    description: str = ""
    category: str
    starts_at: datetime.datetime
    ends_at: datetime.datetime
    location: str = "TBD"

class EventOut(EventCreate):
    id: int
    created_by: int
    class Config:
        from_attributes = True

class RSVPCreate(BaseModel):
    status: str = "going"

class RSVPOut(BaseModel):
    id: int
    event_id: int
    user_id: int
    status: str
    created_at: datetime.datetime
    class Config:
        from_attributes = True

# ---------- Placement ----------
class PlacementCreate(BaseModel):
    company: str
    role: str
    description: str = ""
    deadline: datetime.datetime

class PlacementOut(PlacementCreate):
    id: int
    posted_by: int
    class Config:
        from_attributes = True

class AlumniExperienceCreate(BaseModel):
    company: str
    content: str

class AlumniExperienceOut(AlumniExperienceCreate):
    id: int
    alumni_id: int
    created_at: datetime.datetime
    class Config:
        from_attributes = True

# ---------- Marketplace ----------
class ListingCreate(BaseModel):
    title: str
    description: str
    price: float = 0.0
    category: str

class ListingOut(ListingCreate):
    id: int
    owner_id: int
    created_at: datetime.datetime
    class Config:
        from_attributes = True

class MessageCreate(BaseModel):
    receiver_id: int
    content: str

class MessageOut(BaseModel):
    id: int
    listing_id: int
    sender_id: int
    receiver_id: int
    content: str
    created_at: datetime.datetime
    class Config:
        from_attributes = True

# ---------- Alumni / Mentorship ----------
class MentorshipCreate(BaseModel):
    mentee_id: int
    topic: str

class MentorshipOut(BaseModel):
    id: int
    mentor_id: int
    mentee_id: int
    topic: str
    status: str
    class Config:
        from_attributes = True

# ---------- Lost & Found ----------
class LostFoundCreate(BaseModel):
    type: str  # lost or found
    title: str
    description: str = ""
    contact: str = ""

class LostFoundOut(LostFoundCreate):
    id: int
    user_id: int
    created_at: datetime.datetime
    class Config:
        from_attributes = True

# ---------- Hackathons ----------
class HackathonCreate(BaseModel):
    name: str
    description: str = ""
    starts_at: datetime.datetime
    ends_at: datetime.datetime

class HackathonOut(HackathonCreate):
    id: int
    class Config:
        from_attributes = True

class TeamCreate(BaseModel):
    name: str

class TeamOut(BaseModel):
    id: int
    hackathon_id: int
    name: str
    class Config:
        from_attributes = True

class LeaderboardUpdate(BaseModel):
    team_id: int
    score: float

class LeaderboardOut(BaseModel):
    id: int
    hackathon_id: int
    team_id: int
    score: float
    class Config:
        from_attributes = True

# ---------- Moderation ----------
class ReportCreate(BaseModel):
    target_type: str
    target_id: int
    reason: str

class ReportOut(ReportCreate):
    id: int
    reporter_id: int
    status: str
    created_at: datetime.datetime
    class Config:
        from_attributes = True
