# Datei: backend/app/crud/asset_type.py
from app.crud.base import CRUDBase
from app.models import AssetType
from app.schemas import AssetTypeCreate, AssetTypeUpdate

class CRUDAssetType(CRUDBase[AssetType, AssetTypeCreate, AssetTypeUpdate]):
    # Hier können später modellspezifische CRUD-Methoden hinzugefügt werden.
    pass

# Wichtig: Erstelle eine Instanz, die in der API verwendet wird.
asset_type = CRUDAssetType(AssetType)
