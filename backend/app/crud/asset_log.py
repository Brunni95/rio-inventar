# Datei: backend/app/crud/asset_log.py

from typing import List
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import AssetLog
from app.schemas import AssetLogCreate, AssetLogUpdate  # Wir brauchen ein Update-Schema

class CRUDAssetLog(CRUDBase[AssetLog, AssetLogCreate, AssetLogUpdate]):
    def get_by_asset(self, db: Session, *, asset_id: int) -> List[AssetLog]:
        """
        Ruft alle Log-Einträge für ein bestimmtes Asset ab.
        """
        return db.query(AssetLog).filter(AssetLog.asset_id == asset_id).order_by(AssetLog.timestamp.desc()).all()

# WICHTIG: Erstelle die Instanz, die in __init__.py importiert wird.
asset_log = CRUDAssetLog(AssetLog)