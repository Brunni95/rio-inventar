# Datei: backend/app/api/v1/endpoints/suppliers.py
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
    Ruft eine Liste von suppliers ab.
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
    Erstellt einen neuen supplier.
    """
    return crud.supplier.create(db=db, obj_in=item_in)

@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(supplier_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Löscht einen supplier.
    """
    # Verhindere Löschen, wenn Assets auf diesen Lieferanten verweisen
    asset_dependency = db.query(models.Asset).filter(models.Asset.supplier_id == supplier_id).first()
    if asset_dependency:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Supplier mit ID {supplier_id} ist noch bei einem Asset in Verwendung und kann nicht gelöscht werden."
        )

    db_item = crud.supplier.remove(db=db, id=supplier_id)

    if not db_item:
        raise HTTPException(status_code=404, detail="Supplier not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
