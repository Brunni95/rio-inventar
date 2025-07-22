from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import schemas
import crud
from db.session import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Supplier)
def create_supplier(supplier: schemas.SupplierCreate, db: Session = Depends(get_db)):
    return crud.supplier.create_supplier(db=db, supplier=supplier)

@router.get("/", response_model=List[schemas.Supplier])
def read_suppliers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.supplier.get_suppliers(db, skip=skip, limit=limit)
