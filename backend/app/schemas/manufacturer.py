# Datei: backend/app/schemas/manufacturer.py
from pydantic import BaseModel
from typing import Optional

class ManufacturerBase(BaseModel):
    name: str

class ManufacturerCreate(ManufacturerBase):
    pass

# Update-Schema mit optionalem Namen
class ManufacturerUpdate(BaseModel):
    name: Optional[str] = None

class Manufacturer(ManufacturerBase):
    id: int

    class Config:
        from_attributes = True
