from pydantic import BaseModel

# Basis-Attribute eines Artikels
class ItemBase(BaseModel):
    name: str
    sku: str
    description: str | None = None
    quantity: int = 0

# Schema zum Erstellen eines neuen Artikels
class ItemCreate(ItemBase):
    pass

# Schema zum Lesen eines Artikels aus der DB
class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True