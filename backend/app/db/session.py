# in backend/app/db/session.py

from sqlalchemy import create_engine
from app.core.config import DATABASE_URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# NEU: Die get_db-Funktion von main.py hierher verschieben
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()