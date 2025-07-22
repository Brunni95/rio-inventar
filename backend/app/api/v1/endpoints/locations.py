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

@router.post("/", response_model=schemas.Location)
def create_location(location: schemas.LocationCreate, db: Session = Depends(get_db)):
    return crud.location.create_location(db=db, location=location)

@router.get("/", response_model=List[schemas.Location])
def read_locations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    locations = crud.location.get_locations(db, skip=skip, limit=limit)
    return locations






