"""Supplier CRUD endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, models, schemas
from app.db.session import get_db
from app.auth import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[schemas.Supplier])
def read_suppliers(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Return a list of suppliers with pagination.

    Parameters:
    - db: SQLAlchemy session dependency
    - skip: Number of items to skip (offset)
    - limit: Max items to return
    - current_user: Authenticated user dependency
    """
    items = crud.supplier.get_multi(db, skip=skip, limit=limit)
    return items

@router.post("/", response_model=schemas.Supplier, status_code=status.HTTP_201_CREATED)
def create_supplier(
    *,
    db: Session = Depends(get_db),
    item_in: schemas.SupplierCreate,
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Create a new supplier.

    Parameters:
    - db: SQLAlchemy session dependency
    - item_in: Supplier payload
    - current_user: Authenticated user dependency
    """
    return crud.supplier.create(db=db, obj_in=item_in)

@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(supplier_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Delete a supplier. Returns 409 if any asset references it.

    Parameters:
    - supplier_id: Supplier primary key
    - db: SQLAlchemy session dependency
    - current_user: Authenticated user dependency

    Returns:
    - 204 No Content on success

    Raises:
    - HTTPException 404: If supplier does not exist
    - HTTPException 409: If still referenced by assets
    """
    from app.api.utils import ensure_not_in_use
    ensure_not_in_use(db, model=models.Asset, fk_column=models.Asset.supplier_id, fk_id=supplier_id, entity_label="Supplier")

    db_item = crud.supplier.remove(db=db, id=supplier_id)

    if not db_item:
        raise HTTPException(status_code=404, detail="Supplier not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
