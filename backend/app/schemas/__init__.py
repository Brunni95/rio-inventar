# Datei: backend/app/schemas/__init__.py

# Importiere die Schemas aus ihren jeweiligen Dateien,
# damit sie direkt über 'schemas.XXX' verfügbar sind.

from .location import Location, LocationCreate, LocationUpdate
from .manufacturer import Manufacturer, ManufacturerCreate, ManufacturerUpdate
from .status import Status, StatusCreate, StatusUpdate
from .supplier import Supplier, SupplierCreate, SupplierUpdate

# HIER IST DIE KORREKTUR: UserUpdate wird jetzt auch exportiert.
from .user import User, UserCreate, UserUpdate

from .asset_type import AssetType, AssetTypeCreate, AssetTypeUpdate
from .asset import Asset, AssetCreate, AssetUpdate
from .asset_log import AssetLog, AssetLogCreate, AssetLogUpdate