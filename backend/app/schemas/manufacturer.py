from pydantic import BaseModel

class ManufacturerBase(BaseModel):
    name: str

class ManufacturerCreate(ManufacturerBase):
    pass

class Manufacturer(ManufacturerBase):
    id: int

    class Config:
        from_attributes = True