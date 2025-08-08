# Datei: backend/app/api/v1/endpoints/locations.py
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, models, schemas
from app.db.session import get_db
from app.auth import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[schemas.Location])
def read_locations(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Ruft eine Liste von locations ab.
    """
    items = crud.location.get_multi(db, skip=skip, limit=limit)
    return items

@router.post("/", response_model=schemas.Location, status_code=status.HTTP_201_CREATED)
def create_location(
    *,
    db: Session = Depends(get_db),
    item_in: schemas.LocationCreate,
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Erstellt einen neuen location.
    """
    return crud.location.create(db=db, obj_in=item_in)

@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(location_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Löscht einen location.
    """
    # Verhindere Löschen, wenn Assets auf diese Location verweisen
    asset_dependency = db.query(models.Asset).filter(models.Asset.location_id == location_id).first()
    if asset_dependency:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Location mit ID {location_id} ist noch bei einem Asset in Verwendung und kann nicht gelöscht werden."
        )

    db_item = crud.location.remove(db=db, id=location_id)

    if not db_item:
        raise HTTPException(status_code=404, detail="Location not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
