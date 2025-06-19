# SQLAlchemy is a library that provides a way to interact with databases using Python.
# connection for the database

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# format of the database url-- postgresql://username:password@host:port/database_name
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:11825114@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 