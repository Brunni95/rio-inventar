from pydantic import BaseModel

class AssetTypeBase(BaseModel):
    name: str

class AssetTypeCreate(AssetTypeBase):
    pass

class AssetType(AssetTypeBase):
    id: int

    class Config:
        from_attributes = True
