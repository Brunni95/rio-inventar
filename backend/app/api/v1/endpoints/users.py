"""User CRUD endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, models, schemas
from app.db.session import get_db
from app.auth import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Return a list of users with pagination.

    Parameters:
    - db: SQLAlchemy session dependency
    - skip: Number of items to skip (offset)
    - limit: Max items to return
    - current_user: Authenticated user dependency
    """
    items = crud.user.get_multi(db, skip=skip, limit=limit)
    return items

@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(
    *,
    db: Session = Depends(get_db),
    item_in: schemas.UserCreate,
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Create a new user.

    Parameters:
    - db: SQLAlchemy session dependency
    - item_in: User payload
    - current_user: Authenticated user dependency
    """
    return crud.user.create(db=db, obj_in=item_in)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Delete a user. Returns 409 if any asset references them.

    Parameters:
    - user_id: User primary key
    - db: SQLAlchemy session dependency
    - current_user: Authenticated user dependency

    Returns:
    - 204 No Content on success

    Raises:
    - HTTPException 404: If user does not exist
    - HTTPException 409: If still referenced by assets
    """
    from app.api.utils import ensure_not_in_use
    ensure_not_in_use(db, model=models.Asset, fk_column=models.Asset.user_id, fk_id=user_id, entity_label="User")

    db_item = crud.user.remove(db=db, id=user_id)

    if not db_item:
        raise HTTPException(status_code=404, detail="User not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
