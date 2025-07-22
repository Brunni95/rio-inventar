from sqlalchemy.orm import Session
from app import models
from app import schemas

def get_status(db: Session, status_id: int):
    return db.query(models.Status).filter(models.Status.id == status_id).first()

def get_statuses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Status).offset(skip).limit(limit).all()

def create_status(db: Session, status: schemas.StatusCreate):
    db_status = models.Status(**status.model_dump())
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status

