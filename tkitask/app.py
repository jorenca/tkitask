from fastapi import FastAPI, Depends
from sqlalchemy.orm import sessionmaker, Session
from  sqlalchemy.sql.expression import func

from tkitask.create_db_engine import db_engine
from tkitask.question import Question


app = FastAPI()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/question")
def read_item(round: str, value: str, db: Session = Depends(get_db)):

    questions_query = db.query(Question).filter(
        Question.round == round,
        Question.value == value
    ).order_by(func.random())

    return questions_query.first()
