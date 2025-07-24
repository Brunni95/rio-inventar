# Datei: backend/app/schemas/status.py
from pydantic import BaseModel
from typing import Optional

class StatusBase(BaseModel):
    name: str

class StatusCreate(StatusBase):
    pass

# Update-Schema mit optionalem Namen
class StatusUpdate(BaseModel):
    name: Optional[str] = None

class Status(StatusBase):
    id: int

    class Config:
        from_attributes = True
