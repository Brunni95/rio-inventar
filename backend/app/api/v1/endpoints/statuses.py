# Datei: backend/app/api/v1/endpoints/statuses.py
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
    Ruft eine Liste von statuses ab.
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
    Erstellt einen neuen status.
    """
    return crud.status.create(db=db, obj_in=item_in)

@router.delete("/{status_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_status(status_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Löscht einen status.
    """
    # Verhindere Löschen, wenn Assets auf diesen Status verweisen
    asset_dependency = db.query(models.Asset).filter(models.Asset.status_id == status_id).first()
    if asset_dependency:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Status mit ID {status_id} ist noch bei einem Asset in Verwendung und kann nicht gelöscht werden."
        )

    db_item = crud.status.remove(db=db, id=status_id)

    if not db_item:
        raise HTTPException(status_code=404, detail="Status not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
