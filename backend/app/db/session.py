from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Die URL zur Datenbank aus den Umgebungsvariablen von docker-compose.yml
DATABASE_URL = "postgresql://user:password@db:5432/inventardb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()