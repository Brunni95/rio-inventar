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

@router.post("/", response_model=schemas.Manufacturer)
def create_manufacturer(manufacturer: schemas.ManufacturerCreate, db: Session = Depends(get_db)):
    return crud.manufacturer.create_manufacturer(db=db, manufacturer=manufacturer)

@router.get("/", response_model=List[schemas.Manufacturer])
def read_manufacturers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.manufacturer.get_manufacturers(db, skip=skip, limit=limit)






