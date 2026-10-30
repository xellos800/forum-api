from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from . import models
from .config import settings
import time
import psycopg
from psycopg.rows import dict_row
from pydantic_settings import BaseSettings

DATABASE_URL = f'postgresql+psycopg://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}'

engine = create_engine(DATABASE_URL, echo=True)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg.connect(
#             "host=localhost dbname=fastapi user=postgres password=hello", row_factory=dict_row)
#         cur = conn.cursor()
#         print("Database connection successful!")
#         break
#     except Exception as error:
#         print("Could not connect to database: ", error)
#         time.sleep(2)
