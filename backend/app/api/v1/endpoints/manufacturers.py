# Datei: backend/app/api/v1/endpoints/manufacturers.py
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, models, schemas
from app.db.session import get_db
from app.auth import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[schemas.Manufacturer])
def read_manufacturers(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Ruft eine Liste von manufacturers ab.
    """
    items = crud.manufacturer.get_multi(db, skip=skip, limit=limit)
    return items

@router.post("/", response_model=schemas.Manufacturer, status_code=status.HTTP_201_CREATED)
def create_manufacturer(
    *,
    db: Session = Depends(get_db),
    item_in: schemas.ManufacturerCreate,
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Erstellt einen neuen manufacturer.
    """
    return crud.manufacturer.create(db=db, obj_in=item_in)

@router.delete("/{manufacturer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_manufacturer(manufacturer_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Löscht einen manufacturer.
    """
    # KORREKTE PYTHON-SYNTAX: '!=' und ':'
    if "Manufacturer" != "User":
        asset_dependency = db.query(models.Asset).filter(getattr(models.Asset, 'manufacturer_id') == manufacturer_id).first()
        if asset_dependency:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Manufacturer mit ID {manufacturer_id} ist noch bei einem Asset in Verwendung und kann nicht gelöscht werden."
            )

    db_item = crud.manufacturer.remove(db=db, id=manufacturer_id)

    if not db_item:
        raise HTTPException(status_code=404, detail="Manufacturer not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
