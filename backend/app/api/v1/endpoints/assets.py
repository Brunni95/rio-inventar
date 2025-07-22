from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import schemas
import crud
from db.session import get_db
from auth import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.Asset, status_code=201)
def create_asset(asset: schemas.AssetCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return crud.asset.create_asset(db=db, asset=asset)

@router.get("/", response_model=List[schemas.Asset])
def read_assets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    assets = crud.asset.get_assets(db, skip=skip, limit=limit)
    return assets

@router.get("/{asset_id}", response_model=schemas.Asset)
def read_asset(asset_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_asset = crud.asset.get_asset(db, asset_id=asset_id)
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return db_asset

@router.put("/{asset_id}", response_model=schemas.Asset)
def update_asset(asset_id: int, asset_update: schemas.AssetCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_asset = crud.asset.get_asset(db, asset_id=asset_id)
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return crud.asset.update_asset(db=db, db_asset=db_asset, asset_update=asset_update)

@router.delete("/{asset_id}", status_code=204)
def delete_asset(asset_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_asset = crud.asset.get_asset(db, asset_id=asset_id)
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    crud.asset.delete_asset(db=db, db_asset=db_asset)
    return
