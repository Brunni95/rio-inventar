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

@router.post("/", response_model=schemas.Status)
def create_status(status: schemas.StatusCreate, db: Session = Depends(get_db)):
    return crud.status.create_status(db=db, status=status)

@router.get("/", response_model=List[schemas.Status])
def read_statuses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.status.get_statuses(db, skip=skip, limit=limit)






