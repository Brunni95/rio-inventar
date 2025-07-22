from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import schemas
import crud
from db.session import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Manufacturer)
def create_manufacturer(manufacturer: schemas.ManufacturerCreate, db: Session = Depends(get_db)):
    return crud.manufacturer.create_manufacturer(db=db, manufacturer=manufacturer)

@router.get("/", response_model=List[schemas.Manufacturer])
def read_manufacturers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.manufacturer.get_manufacturers(db, skip=skip, limit=limit)
