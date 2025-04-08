import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


load_dotenv()

db_user = os.getenv('SQL_SERVER_USERNAME')
db_pass = os.getenv('SQL_SERVER_PASSWORD')
db_address = os.getenv('SQL_SERVER_ADDRESS')
assert db_user, 'DB server user not set'
assert db_pass, 'DB server password not set'
assert db_address, 'DB server address not set'

url = URL.create(
    drivername="postgresql",
    username=db_user,
    password=db_pass,
    host=db_address,
    database="tkidb"
)

db_engine = create_engine(url)