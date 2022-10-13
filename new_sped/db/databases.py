import os
from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv

load_dotenv()

db_host = os.environ.get("POSTGRES_HOST")
db_name = os.environ.get("POSTGRES_NAME")
db_password = os.environ.get("POSTGRES_PASSWORD")
db_user = os.environ.get("POSTGRES_USER")

print(f'nomes do env: name: {db_name}, host: {db_host}, password: {db_password}, user: {db_user}')

database = f"postgresql://{db_user}:{db_password}@localhost:5432/{db_name}"

engine = create_engine(database, echo=True)


def create_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
