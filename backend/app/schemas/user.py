# Datei: backend/app/schemas/user.py
from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: Optional[str] = None
    display_name: Optional[str] = None
    department: Optional[str] = None
    azure_oid: str

class UserCreate(UserBase):
    pass

# Update-Klasse mit optionalen Feldern
class UserUpdate(BaseModel):
    email: Optional[str] = None
    display_name: Optional[str] = None
    department: Optional[str] = None

class User(UserBase):
    id: int

    class Config:
        from_attributes = True