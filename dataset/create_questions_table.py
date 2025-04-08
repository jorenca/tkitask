from tkitask.create_db_engine import db_engine
from tkitask.question import Base


Base.metadata.create_all(db_engine)