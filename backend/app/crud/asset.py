"""Asset CRUD with search, sorting, pagination and change logging."""

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from typing import Any, Dict, List, Union
from pydantic import BaseModel

from app.crud.base import CRUDBase
from app.models import Asset, AssetLog, User, AssetType, Manufacturer, Location, Status
from app.schemas import AssetCreate, AssetUpdate

class CRUDAsset(CRUDBase[Asset, AssetCreate, AssetUpdate]):
    # get_multi_with_search, create_with_log, und update_with_log bleiben unverändert...
    def _base_query(self, db: Session, *, search: str | None = None):
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
            .join(AssetType, AssetType.id == self.model.asset_type_id, isouter=True)
            .join(Manufacturer, Manufacturer.id == self.model.manufacturer_id, isouter=True)
            .join(Location, Location.id == self.model.location_id, isouter=True)
            .join(Status, Status.id == self.model.status_id, isouter=True)
        )
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Asset.inventory_number.ilike(search_term),
                    Asset.model.ilike(search_term),
                    Asset.hostname.ilike(search_term),
                    Asset.serial_number.ilike(search_term),
                    User.display_name.ilike(search_term),
                    Manufacturer.name.ilike(search_term),
                    Location.name.ilike(search_term),
                )
            )
        return query

    def get_multi_with_search(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        search: str | None = None,
        order_by: str = "id",
        order_dir: str = "desc",
    ) -> List[Asset]:
        query = self._base_query(db, search=search)

        order_map: dict[str, Any] = {
            "id": Asset.id,
            "inventory_number": Asset.inventory_number,
            "model": Asset.model,
            "hostname": Asset.hostname,
            "serial_number": Asset.serial_number,
            "asset_type.name": AssetType.name,
            "manufacturer.name": Manufacturer.name,
            "location.name": Location.name,
            "status.name": Status.name,
            "user.display_name": User.display_name,
        }
        order_col = order_map.get(order_by, Asset.id)
        if (order_dir or "").lower() == "asc":
            query = query.order_by(order_col.asc(), Asset.id.asc())
        else:
            query = query.order_by(order_col.desc(), Asset.id.desc())

        return query.offset(skip).limit(limit).all()

    def count_with_search(self, db: Session, *, search: str | None = None) -> int:
        return self._base_query(db, search=search).count()

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

    def remove(self, db: Session, *, id: int) -> Asset:
        """Delete an asset and all its dependent log entries."""
        db_obj = db.query(self.model).get(id)
        if db_obj:
            # Delete dependent logs first
            db.query(AssetLog).filter(AssetLog.asset_id == id).delete(synchronize_session=False)
            # Then delete the asset itself
            db.delete(db_obj)
            db.commit()
        return db_obj

# Export instance used across the app
asset = CRUDAsset(Asset)