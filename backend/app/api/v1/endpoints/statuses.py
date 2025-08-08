"""Status CRUD endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, models, schemas
from app.db.session import get_db
from app.auth import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[schemas.Status])
def read_statuses(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Return a list of statuses with pagination.

    Parameters:
    - db: SQLAlchemy session dependency
    - skip: Number of items to skip (offset)
    - limit: Max items to return
    - current_user: Authenticated user dependency
    """
    items = crud.status.get_multi(db, skip=skip, limit=limit)
    return items

@router.post("/", response_model=schemas.Status, status_code=status.HTTP_201_CREATED)
def create_status(
    *,
    db: Session = Depends(get_db),
    item_in: schemas.StatusCreate,
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Create a new status.

    Parameters:
    - db: SQLAlchemy session dependency
    - item_in: Status payload
    - current_user: Authenticated user dependency
    """
    return crud.status.create(db=db, obj_in=item_in)

@router.delete("/{status_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_status(status_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Delete a status. Returns 409 if any asset references it.

    Parameters:
    - status_id: Status primary key
    - db: SQLAlchemy session dependency
    - current_user: Authenticated user dependency

    Returns:
    - 204 No Content on success

    Raises:
    - HTTPException 404: If status does not exist
    - HTTPException 409: If still referenced by assets
    """
    from app.api.utils import ensure_not_in_use
    ensure_not_in_use(db, model=models.Asset, fk_column=models.Asset.status_id, fk_id=status_id, entity_label="Status")

    db_item = crud.status.remove(db=db, id=status_id)

    if not db_item:
        raise HTTPException(status_code=404, detail="Status not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
