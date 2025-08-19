from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from app.db import get_db
from app import models, schemas
from app.deps import get_current_user
from app.utils import calculate_gpa, generate_timetable

router = APIRouter()

@router.post("/gpa")
def gpa(payload: Dict):
    # payload: { "courses": [{"credits": x, "grade": "A"}, ...] }
    courses = payload.get("courses", [])
    return {"gpa": calculate_gpa(courses)}

@router.post("/timetable")
def timetable(payload: Dict):
    # payload: { "subjects": ["DBMS","OS", ...] }
    subs = payload.get("subjects", [])
    return generate_timetable(subs)

@router.get("/classroom_locator")
def classroom_locator(building: str, room: str):
    # Placeholder resolver
    return {"building": building, "room": room, "map_url": f"https://maps.example.com/campus?b={building}&r={room}"}
