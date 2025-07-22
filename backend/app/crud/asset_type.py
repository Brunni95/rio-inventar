from sqlalchemy.orm import Session
from app import models
from app import schemas

def get_asset_type(db: Session, asset_type_id: int):
    return db.query(models.AssetType).filter(models.AssetType.id == asset_type_id).first()

def get_asset_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.AssetType).offset(skip).limit(limit).all()

def create_asset_type(db: Session, asset_type: schemas.AssetTypeCreate):
    db_asset_type = models.AssetType(**asset_type.model_dump())
    db.add(db_asset_type)
    db.commit()
    db.refresh(db_asset_type)
    return db_asset_type

