import csv

from sqlalchemy.orm import sessionmaker

from tkitask.create_db_engine import db_engine
from tkitask.question import Question


Session = sessionmaker(bind=db_engine)
session = Session()


with open('dataset.csv', 'r') as dataset_csv:
    reader = csv.DictReader(dataset_csv)  # Read CSV file as dictionary (header row will be used)

    for row in reader:  # not using a comprehension to avoid loading the entire list in memory
        row = {k.strip(): v.strip() for k, v in row.items()}

        value_int = row['Value'].strip('$').replace(',', '')
        if value_int == 'None':  # Discard troll rows
            continue

        if int(value_int) > 1200:
            continue

        new_question = Question(  # This parsing could potentially be done automatically via pydantic
            round=row['Round'],
            category=row['Category'],
            value=row['Value'],  # I'm tempted to strip out leading $ and store as int, but will leave as it is for simplicity
            question=row['Question'],
            answer=row['Answer']
        )
        session.add(new_question)

session.commit()
session.close()