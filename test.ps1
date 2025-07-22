# PowerShell-Skript zur finalen Korrektur der Schema-Importe

Write-Host "🚀 Korrigiere die Schema-Dateien und -Importe..." -ForegroundColor Cyan

# --- Pfad definieren ---
$schemasPath = ".\backend\app\schemas"

# --- 1. Die fehlende Datei schemas/asset_type.py erstellen ---
Write-Host "Erstelle die fehlende Datei schemas/asset_type.py..."
$schemaAssetTypeContent = @"
from pydantic import BaseModel

class AssetTypeBase(BaseModel):
    name: str

class AssetTypeCreate(AssetTypeBase):
    pass

class AssetType(AssetTypeBase):
    id: int

    class Config:
        from_attributes = True
"@
Set-Content -Path "$schemasPath\asset_type.py" -Value $schemaAssetTypeContent

# --- 2. schemas/asset.py aufräumen und korrigieren ---
Write-Host "Korrigiere schemas/asset.py..."
$schemaAssetContent = @"
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
"@
Set-Content -Path "$schemasPath\asset.py" -Value $schemaAssetContent

# --- 3. schemas/__init__.py sicherstellen, dass alles korrekt ist ---
Write-Host "Aktualisiere schemas/__init__.py..."
$initContent = @"
from .asset import Asset, AssetCreate
from .asset_type import AssetType, AssetTypeCreate
from .location import Location, LocationCreate
from .manufacturer import Manufacturer, ManufacturerCreate
from .status import Status, StatusCreate
from .supplier import Supplier, SupplierCreate
from .user import User, UserCreate
from .asset_log import AssetLog, AssetLogCreate
"@
Set-Content -Path "$schemasPath\__init__.py" -Value $initContent

Write-Host "✅ Schema-Struktur erfolgreich korrigiert! Du kannst die App jetzt neu starten." -ForegroundColor Green