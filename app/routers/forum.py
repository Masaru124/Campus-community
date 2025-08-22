from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app import models, schemas
from app.deps import get_current_user

router = APIRouter()

@router.post("/posts", response_model=schemas.PostOut)
def create_post(payload: schemas.PostCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    # Use the Question model but treat it as a simple post
    q = models.Question(title=payload.title, body=payload.content, tags="", author_id=user.id)
    db.add(q); db.commit(); db.refresh(q)
    return schemas.PostOut(id=q.id, title=q.title, content=q.body, author_id=q.author_id, created_at=q.created_at, upvotes=q.upvotes)

@router.get("/posts", response_model=List[schemas.PostOut])
def list_posts(db: Session = Depends(get_db)):
    data = db.query(models.Question).order_by(models.Question.created_at.desc()).all()
    return [schemas.PostOut(id=q.id, title=q.title, content=q.body, author_id=q.author_id, created_at=q.created_at, upvotes=q.upvotes) for q in data]

@router.post("/questions", response_model=schemas.QuestionOut)
def create_question(payload: schemas.QuestionCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    q = models.Question(title=payload.title, body=payload.body, tags=",".join(payload.tags), author_id=user.id)
    db.add(q); db.commit(); db.refresh(q)
    return schemas.QuestionOut(id=q.id, title=q.title, body=q.body, tags=q.tags.split(",") if q.tags else [], author_id=q.author_id, created_at=q.created_at, upvotes=q.upvotes)

@router.get("/questions", response_model=List[schemas.QuestionOut])
def list_questions(db: Session = Depends(get_db)):
    data = db.query(models.Question).order_by(models.Question.created_at.desc()).all()
    return [schemas.QuestionOut(id=q.id, title=q.title, body=q.body, tags=q.tags.split(",") if q.tags else [], author_id=q.author_id, created_at=q.created_at, upvotes=q.upvotes) for q in data]

@router.post("/questions/{qid}/upvote")
def upvote_question(qid: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    q = db.query(models.Question).get(qid)
    if not q: raise HTTPException(404, detail="Question not found")
    q.upvotes += 1; db.commit()
    return {"detail": "Upvoted"}

@router.post("/questions/{qid}/answers", response_model=schemas.AnswerOut)
def answer_question(qid: int, payload: schemas.AnswerCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    q = db.query(models.Question).get(qid)
    if not q: raise HTTPException(404, detail="Question not found")
    a = models.Answer(question_id=qid, body=payload.body, author_id=user.id)
    db.add(a); db.commit(); db.refresh(a)
    return a

@router.post("/answers/{aid}/upvote")
def upvote_answer(aid: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    a = db.query(models.Answer).get(aid)
    if not a: raise HTTPException(404, detail="Answer not found")
    a.upvotes += 1; db.commit()
    return {"detail": "Upvoted"}

@router.get("/questions/{qid}/answers", response_model=List[schemas.AnswerOut])
def list_answers(qid: int, db: Session = Depends(get_db)):
    return db.query(models.Answer).filter(models.Answer.question_id == qid).order_by(models.Answer.created_at.asc()).all()
