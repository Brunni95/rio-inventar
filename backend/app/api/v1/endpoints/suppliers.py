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

@router.post("/", response_model=schemas.Supplier)
def create_supplier(supplier: schemas.SupplierCreate, db: Session = Depends(get_db)):
    return crud.supplier.create_supplier(db=db, supplier=supplier)

@router.get("/", response_model=List[schemas.Supplier])
def read_suppliers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.supplier.get_suppliers(db, skip=skip, limit=limit)






