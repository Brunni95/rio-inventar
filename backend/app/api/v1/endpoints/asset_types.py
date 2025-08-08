"""AssetType CRUD endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, models, schemas
from app.db.session import get_db
from app.auth import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[schemas.AssetType])
def read_asset_types(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Return a list of asset types with pagination.

    Parameters:
    - db: SQLAlchemy session dependency
    - skip: Number of items to skip (offset)
    - limit: Max items to return
    - current_user: Authenticated user dependency
    """
    items = crud.asset_type.get_multi(db, skip=skip, limit=limit)
    return items

@router.post("/", response_model=schemas.AssetType, status_code=status.HTTP_201_CREATED)
def create_asset_type(
    *,
    db: Session = Depends(get_db),
    item_in: schemas.AssetTypeCreate,
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Create a new asset type.

    Parameters:
    - db: SQLAlchemy session dependency
    - item_in: AssetType payload
    - current_user: Authenticated user dependency
    """
    return crud.asset_type.create(db=db, obj_in=item_in)

@router.delete("/{asset_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset_type(asset_type_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Delete an asset type. Returns 409 if any asset references it.

    Parameters:
    - asset_type_id: AssetType primary key
    - db: SQLAlchemy session dependency
    - current_user: Authenticated user dependency

    Returns:
    - 204 No Content on success

    Raises:
    - HTTPException 404: If asset type does not exist
    - HTTPException 409: If still referenced by assets
    """
    from app.api.utils import ensure_not_in_use
    ensure_not_in_use(db, model=models.Asset, fk_column=models.Asset.asset_type_id, fk_id=asset_type_id, entity_label="AssetType")

    db_item = crud.asset_type.remove(db=db, id=asset_type_id)

    if not db_item:
        raise HTTPException(status_code=404, detail="AssetType not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
