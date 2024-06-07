# src/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os
sys.path.append('D:/ai-mysticism')
print(sys.path)

from config import settings

DATABASE_URL = settings.database_url
print(DATABASE_URL)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
