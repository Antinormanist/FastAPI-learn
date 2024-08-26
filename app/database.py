from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

DB = config('DB')
DB_USER = config('DB_USER')
DB_USER_PSWRD = config('DB_USER_PSWRD')
DB_HOST = config('DB_HOST')
DB_PORT = config('DB_PORT')
DB_NAME = config('DB_NAME')

engine = create_engine(f'{DB}://{DB_USER}:{DB_USER_PSWRD}@{DB_HOST}:{DB_PORT}/{DB_NAME}', echo=True)
SessionLocal = sessionmaker(engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()