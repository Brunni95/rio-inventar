from sqlalchemy.orm import Session
from app import models, schemas

def get_user_by_azure_oid(db: Session, azure_oid: str):
    return db.query(models.User).filter(models.User.azure_oid == azure_oid).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        azure_oid=user.azure_oid,
        email=user.email,
        display_name=user.display_name,
        department=user.department
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
