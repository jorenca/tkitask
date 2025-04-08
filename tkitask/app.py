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
def get_question(round: str, value: str, db: Session = Depends(get_db)):

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


@app.post("/agent-play/")
def agent_play(db: Session = Depends(get_db)):

    random_question = db.query(Question).order_by(func.random()).first()

    question_prompt = f"""
    Imagine you're a played in the game Jeopardy, and you're given the following question in the "{random_question.round}" round.
    Answer with a single line:
    {random_question.question}
    """
    gpt_answer = ask_gpt(question_prompt)

    return {
        'agent_name': 'ChatGPT',
        'question': random_question.question,
        'ai_answer': gpt_answer,
        'actual_answer': random_question.answer,
        'is_correct': verify_answer(
            VerifyAnswerRequest(
                user_answer=gpt_answer,
                question_id=random_question.question_id
            ),
            db)
    }