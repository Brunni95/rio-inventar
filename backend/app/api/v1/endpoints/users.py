# Datei: backend/app/api/v1/endpoints/users.py
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
    Ruft eine Liste von users ab.
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
    Erstellt einen neuen user.
    """
    return crud.user.create(db=db, obj_in=item_in)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Löscht einen user.
    """
    # KORREKTE PYTHON-SYNTAX: '!=' und ':'
    if "User" != "User":
        asset_dependency = db.query(models.Asset).filter(getattr(models.Asset, 'user_id') == user_id).first()
        if asset_dependency:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User mit ID {user_id} ist noch bei einem Asset in Verwendung und kann nicht gelöscht werden."
            )

    db_item = crud.user.remove(db=db, id=user_id)

    if not db_item:
        raise HTTPException(status_code=404, detail="User not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
