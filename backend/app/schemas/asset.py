from pydantic import BaseModel
from datetime import date
from typing import Optional

# Importiere die fertigen Schemas aus ihren eigenen Dateien
from .location import Location
from .manufacturer import Manufacturer
from .status import Status
from .supplier import Supplier
from .user import User
from .asset_type import AssetType

class AssetBase(BaseModel):
    inventory_number: str
    serial_number: Optional[str] = None
    model: Optional[str] = None
    purchase_price: Optional[float] = None
    department: Optional[str] = None
    os_version: Optional[str] = None
    installation_date: Optional[date] = None
    warranty_expiry: Optional[date] = None
    purchase_date: Optional[date] = None
    notes: Optional[str] = None
    ip_address: Optional[str] = None
    hostname: Optional[str] = None
    mac_address: Optional[str] = None

class AssetCreate(AssetBase):
    asset_type_id: int
    manufacturer_id: int
    status_id: int
    location_id: int
    supplier_id: Optional[int] = None
    user_id: Optional[int] = None

class Asset(AssetBase):
    id: int
    asset_type: AssetType
    manufacturer: Manufacturer
    status: Status
    location: Location
    supplier: Optional[Supplier] = None
    user: Optional[User] = None

    class Config:
        from_attributes = True
