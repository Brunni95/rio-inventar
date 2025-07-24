# Datei: backend/app/schemas/asset_type.py
from pydantic import BaseModel
from typing import Optional

class AssetTypeBase(BaseModel):
    name: str

class AssetTypeCreate(AssetTypeBase):
    pass

# Update-Schema mit optionalem Namen
class AssetTypeUpdate(BaseModel):
    name: Optional[str] = None

class AssetType(AssetTypeBase):
    id: int

    class Config:
        from_attributes = True
