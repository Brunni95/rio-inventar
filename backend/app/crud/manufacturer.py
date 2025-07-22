from sqlalchemy.orm import Session
from app import models
from app import schemas

def get_manufacturer(db: Session, manufacturer_id: int):
    return db.query(models.Manufacturer).filter(models.Manufacturer.id == manufacturer_id).first()

def get_manufacturers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Manufacturer).offset(skip).limit(limit).all()

def create_manufacturer(db: Session, manufacturer: schemas.ManufacturerCreate):
    db_manufacturer = models.Manufacturer(**manufacturer.model_dump())
    db.add(db_manufacturer)
    db.commit()
    db.refresh(db_manufacturer)
    return db_manufacturer

