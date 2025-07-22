from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from app import models, schemas, crud

def get_asset(db: Session, asset_id: int):
    return db.query(models.Asset).filter(models.Asset.id == asset_id).first()

def get_assets(db: Session, skip: int = 0, limit: int = 100, search: str | None = None):
    query = db.query(models.Asset).options(
        joinedload(models.Asset.asset_type),
        joinedload(models.Asset.manufacturer),
        joinedload(models.Asset.status),
        joinedload(models.Asset.location),
        joinedload(models.Asset.supplier),
        joinedload(models.Asset.user)
    )
    if search:
        search_term = f"%{search}%"
        query = query.join(models.Manufacturer).join(models.Location).join(models.User, isouter=True).filter(
            or_(
                models.Asset.inventory_number.ilike(search_term),
                models.Asset.serial_number.ilike(search_term),
                models.Asset.model.ilike(search_term),
                models.User.display_name.ilike(search_term),
                models.Manufacturer.name.ilike(search_term),
                models.Location.name.ilike(search_term)
            )
        )
    return query.offset(skip).limit(limit).all()

def create_asset(db: Session, asset: schemas.AssetCreate, user_id: int):
    db_asset = models.Asset(**asset.model_dump())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)

    # --- NEU: Log-Eintrag erstellen ---
    log_entry = schemas.AssetLogCreate(
        action="Asset erstellt",
        asset_id=db_asset.id,
        changed_by_user_id=user_id,
        notes=f"Asset '{db_asset.inventory_number}' wurde erstellt."
    )
    crud.asset_log.create_asset_log(db, log_entry=log_entry)

    return db_asset

def update_asset(db: Session, db_asset: models.Asset, asset_update: schemas.AssetCreate, user_id: int):
    update_data = asset_update.model_dump(exclude_unset=True)
    # Speichere die alten Werte, bevor wir sie ändern
    old_values = {key: getattr(db_asset, key) for key in update_data}

    for key, value in update_data.items():
        setattr(db_asset, key, value)

    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)

    # --- NEU: Log-Einträge für jede einzelne Änderung erstellen ---
    for key, new_value in update_data.items():
        old_value = old_values[key]
        if old_value != new_value:
            log_entry = schemas.AssetLogCreate(
                action="Asset aktualisiert",
                field_changed=key,
                old_value=str(old_value),
                new_value=str(new_value),
                asset_id=db_asset.id,
                changed_by_user_id=user_id
            )
            crud.asset_log.create_asset_log(db, log_entry=log_entry)

    return db_asset

def delete_asset(db: Session, db_asset: models.Asset, user_id: int):
    asset_id = db_asset.id
    inventory_number = db_asset.inventory_number

    # --- NEU: Log-Eintrag erstellen, BEVOR wir das Asset löschen ---
    log_entry = schemas.AssetLogCreate(
        action="Asset gelöscht",
        asset_id=asset_id,
        changed_by_user_id=user_id,
        notes=f"Asset '{inventory_number}' wurde gelöscht."
    )
    crud.asset_log.create_asset_log(db, log_entry=log_entry)

    db.delete(db_asset)
    db.commit()