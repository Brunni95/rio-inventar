"""Manufacturer CRUD endpoints."""
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
    Return a list of manufacturers with pagination.

    Parameters:
    - db: SQLAlchemy session dependency
    - skip: Number of items to skip (offset)
    - limit: Max items to return
    - current_user: Authenticated user dependency
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
    Create a new manufacturer.

    Parameters:
    - db: SQLAlchemy session dependency
    - item_in: Manufacturer payload
    - current_user: Authenticated user dependency
    """
    return crud.manufacturer.create(db=db, obj_in=item_in)

@router.delete("/{manufacturer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_manufacturer(manufacturer_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Delete a manufacturer. Returns 409 if any asset references it.

    Parameters:
    - manufacturer_id: Manufacturer primary key
    - db: SQLAlchemy session dependency
    - current_user: Authenticated user dependency

    Returns:
    - 204 No Content on success

    Raises:
    - HTTPException 404: If manufacturer does not exist
    - HTTPException 409: If still referenced by assets
    """
    from app.api.utils import ensure_not_in_use
    ensure_not_in_use(db, model=models.Asset, fk_column=models.Asset.manufacturer_id, fk_id=manufacturer_id, entity_label="Manufacturer")

    db_item = crud.manufacturer.remove(db=db, id=manufacturer_id)

    if not db_item:
        raise HTTPException(status_code=404, detail="Manufacturer not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
