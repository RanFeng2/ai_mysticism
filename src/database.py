# src/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from config import settings

# DATABASE_URL = settings.database_url
DATABASE_URL = "mysql+pymysql://ai-mysticism:irCCY7ZZY4zrNyz8@8.130.32.234:3306/ai-mysticism"

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
