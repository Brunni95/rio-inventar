"""Location CRUD endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, models, schemas
from app.api.utils import ensure_not_in_use
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
    Return a list of locations with pagination.

    Parameters:
    - db: SQLAlchemy session dependency
    - skip: Number of items to skip (offset)
    - limit: Max items to return
    - current_user: Authenticated user dependency
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
    Create a new location.

    Parameters:
    - db: SQLAlchemy session dependency
    - item_in: Location payload
    - current_user: Authenticated user dependency
    """
    return crud.location.create(db=db, obj_in=item_in)

@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(location_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Delete a location. Returns 409 if any asset references it.

    Parameters:
    - location_id: Location primary key
    - db: SQLAlchemy session dependency
    - current_user: Authenticated user dependency

    Returns:
    - 204 No Content on success

    Raises:
    - HTTPException 404: If location does not exist
    - HTTPException 409: If still referenced by assets
    """
    ensure_not_in_use(db, model=models.Asset, fk_column=models.Asset.location_id, fk_id=location_id, entity_label="Location")

    db_item = crud.location.remove(db=db, id=location_id)

    if not db_item:
        raise HTTPException(status_code=404, detail="Location not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
