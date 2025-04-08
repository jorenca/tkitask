from fastapi import FastAPI, Depends
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql.expression import func
from pydantic import BaseModel

from tkitask.create_db_engine import db_engine
from tkitask.question import Question
from tkitask.prompting import ask_gpt


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


class VerifyAnswerRequest(BaseModel):
    question_id: int
    user_answer: str


@app.post("/verify-answer/")
def verify_answer(answer: VerifyAnswerRequest, db: Session = Depends(get_db)):

    question = db.query(Question).filter_by(question_id=answer.question_id).first()
    if not question:
        return { 'error': f'No question with id {answer.question_id}' }

    verification_prompt = f"""
    You are a helpful assistant that verifies answers to questions.
    You will ignore minor typing errors, garbage characters and phrasing.
    
    Question: {question.question}
    Correct answer: {question.answer}
    User answer: {answer.user_answer}
    
    Respond with a single word - either "correct" or "incorrect".
    """

    gpt_response = ask_gpt(verification_prompt)

    return {
        "is_correct": gpt_response == 'correct',
        "ai_response": gpt_response
    }