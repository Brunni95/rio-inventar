# Datei: backend/app/api/v1/endpoints/assets.py

from fastapi import APIRouter, Depends, HTTPException, Query, status, Response # <-- HIER IST DIE KORREKTUR
from sqlalchemy.orm import Session
from typing import List, Optional

from app import crud, models, schemas
from app.auth import get_current_active_user
from app.db.session import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Asset])
def read_assets(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = Query(None, description="Suche nach Inventarnr, Modell, Hostname oder Benutzername"),
        current_user: models.User = Depends(get_current_active_user)
):
    """
    Ruft eine Liste von Assets ab, mit optionaler Suche.
    """
    assets = crud.asset.get_multi_with_search(db, skip=skip, limit=limit, search=search)
    return assets


@router.post("/", response_model=schemas.Asset, status_code=status.HTTP_201_CREATED)
def create_asset(
        *,
        db: Session = Depends(get_db),
        asset_in: schemas.AssetCreate,
        current_user: models.User = Depends(get_current_active_user)
):
    """
    Erstellt ein neues Asset und protokolliert die Aktion.
    """
    asset = crud.asset.create_with_log(db=db, obj_in=asset_in, user_id=current_user.id)
    return asset


@router.get("/{asset_id}", response_model=schemas.Asset)
def read_asset(
        *,
        db: Session = Depends(get_db),
        asset_id: int,
        current_user: models.User = Depends(get_current_active_user)
):
    """
    Ruft ein einzelnes Asset anhand seiner ID ab.
    """
    asset = crud.asset.get(db=db, id=asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.get("/{asset_id}/logs", response_model=List[schemas.AssetLog])
def read_asset_logs(
        *,
        db: Session = Depends(get_db),
        asset_id: int,
        current_user: models.User = Depends(get_current_active_user)
):
    """
    Ruft die Historie (Logs) für ein bestimmtes Asset ab.
    """
    asset = crud.asset.get(db=db, id=asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return crud.asset_log.get_by_asset(db=db, asset_id=asset_id)


@router.put("/{asset_id}", response_model=schemas.Asset)
def update_asset(
        *,
        db: Session = Depends(get_db),
        asset_id: int,
        asset_in: schemas.AssetUpdate,
        current_user: models.User = Depends(get_current_active_user)
):
    """
    Aktualisiert ein Asset und protokolliert die Änderungen.
    """
    asset = crud.asset.get(db=db, id=asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    asset = crud.asset.update_with_log(db=db, db_obj=asset, obj_in=asset_in, user_id=current_user.id)
    return asset


@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset(
        *,
        db: Session = Depends(get_db),
        asset_id: int,
        current_user: models.User = Depends(get_current_active_user)
):
    """
    Löscht ein Asset.
    """
    asset = crud.asset.get(db=db, id=asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    crud.asset.remove(db=db, id=asset_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)