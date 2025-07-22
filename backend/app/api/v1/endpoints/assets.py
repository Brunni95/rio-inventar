from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, models
from app.db.session import get_db
from app.auth import get_current_active_user

router = APIRouter()

# NEU: Endpunkt, um die Historie eines Assets abzurufen
@router.get("/{asset_id}/logs", response_model=List[schemas.AssetLog])
def read_asset_logs(asset_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    return crud.asset_log.get_logs_for_asset(db, asset_id=asset_id)

@router.post("/", response_model=schemas.Asset, status_code=201)
def create_asset(asset: schemas.AssetCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    return crud.asset.create_asset(db=db, asset=asset, user_id=current_user.id)

@router.get("/", response_model=List[schemas.Asset])
def read_assets(skip: int = 0, limit: int = 100, search: str | None = None, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    return crud.asset.get_assets(db, skip=skip, limit=limit, search=search)

@router.get("/{asset_id}", response_model=schemas.Asset)
def read_asset(asset_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    db_asset = crud.asset.get_asset(db, asset_id=asset_id)
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return db_asset

@router.put("/{asset_id}", response_model=schemas.Asset)
def update_asset(asset_id: int, asset_update: schemas.AssetCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    db_asset = crud.asset.get_asset(db, asset_id=asset_id)
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return crud.asset.update_asset(db=db, db_asset=db_asset, asset_update=asset_update, user_id=current_user.id)

@router.delete("/{asset_id}", status_code=204)
def delete_asset(asset_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    db_asset = crud.asset.get_asset(db, asset_id=asset_id)
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    crud.asset.delete_asset(db=db, db_asset=db_asset, user_id=current_user.id)
    return