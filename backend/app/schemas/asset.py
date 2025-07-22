from pydantic import BaseModel
from datetime import date

# Importiere die fertigen Schemas, die wir gerade erstellt haben
from .location import Location
from .manufacturer import Manufacturer
from .status import Status
from .supplier import Supplier

class AssetBase(BaseModel):
    inventory_number: str
    serial_number: str | None = None
    model: str | None = None
    assigned_to: str | None = None
    department: str | None = None
    os_version: str | None = None
    installation_date: date | None = None
    warranty_expiry: date | None = None
    purchase_date: date | None = None
    notes: str | None = None
    ip_address: str | None = None
    hostname: str | None = None
    mac_address: str | None = None

class AssetCreate(AssetBase):
    # Beim Erstellen übergeben wir nur die IDs der verknüpften Objekte
    asset_type_id: int
    manufacturer_id: int
    status_id: int
    location_id: int
    supplier_id: int | None = None

class Asset(AssetBase):
    id: int
    # Beim Auslesen wollen wir die kompletten, verschachtelten Objekte sehen
    asset_type: BaseModel # Temporär, wird unten ersetzt
    manufacturer: Manufacturer
    status: Status
    location: Location
    supplier: Supplier | None = None

    class Config:
        from_attributes = True

# Wir brauchen noch ein Schema für AssetType, das in Asset verwendet wird
class AssetTypeBase(BaseModel):
    name: str

class AssetTypeCreate(AssetTypeBase):
    pass

class AssetType(AssetTypeBase):
    id: int

    class Config:
        from_attributes = True

# Jetzt, wo AssetType definiert ist, können wir das Asset-Schema finalisieren
Asset.model_rebuild()
Asset.model_fields['asset_type'] = AssetType.model_validate