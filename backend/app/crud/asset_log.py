from sqlalchemy.orm import Session, joinedload
from app import models, schemas

def create_asset_log(db: Session, log_entry: schemas.AssetLogCreate):
    db_log = models.AssetLog(**log_entry.model_dump())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_logs_for_asset(db: Session, asset_id: int):
    return db.query(models.AssetLog).filter(models.AssetLog.asset_id == asset_id).options(joinedload(models.AssetLog.changed_by_user)).order_by(models.AssetLog.timestamp.desc()).all()
