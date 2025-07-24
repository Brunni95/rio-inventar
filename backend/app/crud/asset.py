# Datei: backend/app/crud/asset.py

from sqlalchemy.orm import Session
from sqlalchemy import or_ # WICHTIG: für die Suche benötigt
from typing import Any, Dict, List, Union

from app.crud.base import CRUDBase
from app.models import Asset, AssetLog, User # User-Modell für die Suche importieren
from app.schemas import AssetCreate, AssetUpdate

class CRUDAsset(CRUDBase[Asset, AssetCreate, AssetUpdate]):
    def get_multi_with_search(
            self, db: Session, *, skip: int = 0, limit: int = 100, search: str | None = None
    ) -> List[Asset]:
        """
        Ruft eine Liste von Assets ab, mit optionaler Suche über mehrere Felder.
        """
        # Wir beginnen mit einer Basis-Abfrage.
        # Ein LEFT JOIN (isouter=True) zu User stellt sicher, dass auch Assets
        # ohne zugewiesenen Benutzer gefunden werden.
        query = db.query(self.model).join(User, User.id == self.model.user_id, isouter=True)

        if search:
            # Wenn ein Suchbegriff vorhanden ist, filtern wir.
            # ilike ist eine case-insensitive (ignoriert Gross-/Kleinschreibung) Suche.
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Asset.inventory_number.ilike(search_term),
                    Asset.model.ilike(search_term),
                    Asset.hostname.ilike(search_term),
                    Asset.serial_number.ilike(search_term),
                    User.display_name.ilike(search_term) # Suche im Namen des Benutzers
                )
            )

        # Wende Paginierung an und gib die Resultate zurück.
        return query.order_by(self.model.id.desc()).offset(skip).limit(limit).all()

    def create_with_log(self, db: Session, *, obj_in: AssetCreate, user_id: int) -> Asset:
        """
        Erstellt ein neues Asset und protokolliert diese Aktion.
        """
        # Erstelle das Asset-Objekt mit der Basis-CRUD-Methode
        db_obj = super().create(db, obj_in=obj_in)

        # Erstelle den Log-Eintrag
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
        """
        Aktualisiert ein Asset und protokolliert alle geänderten Felder.
        """
        # Hole die alten Werte, bevor wir sie aktualisieren
        old_data = {c.name: getattr(db_obj, c.name) for c in db_obj.__table__.columns}

        # Aktualisiere das Objekt mit der Basis-CRUD-Methode
        updated_obj = super().update(db, db_obj=db_obj, obj_in=obj_in)

        # Konvertiere das Pydantic-Update-Objekt in ein Dictionary
        if isinstance(obj_in, BaseModel):
            update_data = obj_in.model_dump(exclude_unset=True)
        else:
            update_data = obj_in

        # Vergleiche alte und neue Werte und erstelle Log-Einträge
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

# Erstelle eine Instanz der CRUD-Klasse, die wir in der API verwenden können.
asset = CRUDAsset(Asset)