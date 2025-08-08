# Datei: backend/app/crud/asset.py

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from typing import Any, Dict, List, Union
from pydantic import BaseModel

from app.crud.base import CRUDBase
from app.models import Asset, AssetLog, User
from app.schemas import AssetCreate, AssetUpdate

class CRUDAsset(CRUDBase[Asset, AssetCreate, AssetUpdate]):
    # get_multi_with_search, create_with_log, und update_with_log bleiben unverändert...
    def get_multi_with_search(
            self, db: Session, *, skip: int = 0, limit: int = 100, search: str | None = None
    ) -> List[Asset]:
        # Eager Loading für verbundene Relationen, um N+1 zu vermeiden
        query = (
            db.query(self.model)
            .options(
                joinedload(Asset.asset_type),
                joinedload(Asset.manufacturer),
                joinedload(Asset.status),
                joinedload(Asset.location),
                joinedload(Asset.supplier),
                joinedload(Asset.user),
            )
            .join(User, User.id == self.model.user_id, isouter=True)
        )
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Asset.inventory_number.ilike(search_term),
                    Asset.model.ilike(search_term),
                    Asset.hostname.ilike(search_term),
                    Asset.serial_number.ilike(search_term),
                    User.display_name.ilike(search_term)
                )
            )
        return query.order_by(self.model.id.desc()).offset(skip).limit(limit).all()

    def create_with_log(self, db: Session, *, obj_in: AssetCreate, user_id: int) -> Asset:
        db_obj = super().create(db, obj_in=obj_in)
        log_entry = AssetLog(
            asset_id=db_obj.id,
            changed_by_user_id=user_id,
            action="CREATE",
            notes=f"Asset '{db_obj.inventory_number}' wurde erstellt."
        )
        db.add(log_entry)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_with_log(
            self, db: Session, *, db_obj: Asset, obj_in: Union[AssetUpdate, Dict[str, Any]], user_id: int
    ) -> Asset:
        old_data = {c.name: getattr(db_obj, c.name) for c in db_obj.__table__.columns}
        updated_obj = super().update(db, db_obj=db_obj, obj_in=obj_in)
        if isinstance(obj_in, BaseModel):
            update_data = obj_in.model_dump(exclude_unset=True)
        else:
            update_data = obj_in
        for field, new_value in update_data.items():
            old_value = old_data.get(field)
            if old_value != new_value:
                log_entry = AssetLog(
                    asset_id=db_obj.id,
                    changed_by_user_id=user_id,
                    action="UPDATE",
                    field_changed=field,
                    old_value=str(old_value),
                    new_value=str(new_value)
                )
                db.add(log_entry)
        db.commit()
        db.refresh(updated_obj)
        return updated_obj

    # ==========================================================
    # HIER IST DIE NEUE, ÜBERSCHRIEBENE METHODE
    # ==========================================================
    def remove(self, db: Session, *, id: int) -> Asset:
        """
        Löscht ein Asset und alle dazugehörigen Log-Einträge.
        """
        # Finde zuerst das Objekt, das wir löschen wollen
        db_obj = db.query(self.model).get(id)
        if db_obj:
            # Lösche ZUERST alle abhängigen Log-Einträge
            db.query(AssetLog).filter(AssetLog.asset_id == id).delete(synchronize_session=False)

            # Lösche DANN das Asset selbst
            db.delete(db_obj)
            db.commit()
        return db_obj

# Die Instanz bleibt gleich
asset = CRUDAsset(Asset)