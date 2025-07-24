# Datei: backend/app/api/v1/endpoints/asset_types.py
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
    Ruft eine Liste von asset-types ab.
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
    Erstellt einen neuen asset_type.
    """
    return crud.asset_type.create(db=db, obj_in=item_in)

@router.delete("/{asset_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset_type(asset_type_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Löscht einen asset_type.
    """
    # KORREKTE PYTHON-SYNTAX: '!=' und ':'
    if "AssetType" != "User":
        asset_dependency = db.query(models.Asset).filter(getattr(models.Asset, 'asset_type_id') == asset_type_id).first()
        if asset_dependency:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"AssetType mit ID {asset_type_id} ist noch bei einem Asset in Verwendung und kann nicht gelöscht werden."
            )

    db_item = crud.asset_type.remove(db=db, id=asset_type_id)

    if not db_item:
        raise HTTPException(status_code=404, detail="AssetType not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
