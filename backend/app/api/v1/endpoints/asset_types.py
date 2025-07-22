from app import models
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import models
from app.auth import get_current_active_user
from app import schemas
from app import crud
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=schemas.AssetType)
def create_asset_type(asset_type: schemas.AssetTypeCreate, db: Session = Depends(get_db)):
    return crud.asset_type.create_asset_type(db=db, asset_type=asset_type)

@router.get("/", response_model=List[schemas.AssetType])
def read_asset_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.asset_type.get_asset_types(db, skip=skip, limit=limit)






