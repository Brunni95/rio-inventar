# Datei: backend/app/schemas/location.py
from pydantic import BaseModel
from typing import Optional

class LocationBase(BaseModel):
    name: str

class LocationCreate(LocationBase):
    pass

# Update-Schema mit optionalem Namen
class LocationUpdate(BaseModel):
    name: Optional[str] = None

class Location(LocationBase):
    id: int

    class Config:
        from_attributes = True
