# Datei: backend/app/schemas/supplier.py
from pydantic import BaseModel
from typing import Optional

class SupplierBase(BaseModel):
    name: str

class SupplierCreate(SupplierBase):
    pass

# Update-Schema mit optionalem Namen
class SupplierUpdate(BaseModel):
    name: Optional[str] = None

class Supplier(SupplierBase):
    id: int

    class Config:
        from_attributes = True
