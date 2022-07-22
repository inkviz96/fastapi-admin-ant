from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


engine = create_engine(
    os.getenv("DATABASE_URL")
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()
Base = declarative_base()


def get_db():
    db = SessionLocal()  # 2
    try:
        yield db  # 3
    finally:
        db.close()
