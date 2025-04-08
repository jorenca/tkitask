from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class Question(Base):
    __tablename__ = 'questions'

    question_id = Column('id', Integer, primary_key=True)
    round = Column('round', String, unique=False, nullable=False)
    category = Column('category', String, unique=False, nullable=False)
    value = Column('value', String, unique=False, nullable=False)
    question = Column('question', String, unique=False, nullable=False)
    answer = Column('answer', String, unique=False, nullable=False)

    def __repr__(self):
        return f"<Question(question_id={self.question_id}, round='{self.round}', category='{self.category}' value='{self.value}', question='{self.question}', answer='{self.answer}')>"
