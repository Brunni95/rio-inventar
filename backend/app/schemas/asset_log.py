# Datei: backend/app/schemas/asset_log.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Importiere das User-Schema, um es im Log anzuzeigen
from .user import User

class AssetLogBase(BaseModel):
    asset_id: int
    action: str
    field_changed: Optional[str] = None
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    notes: Optional[str] = None

class AssetLogCreate(AssetLogBase):
    pass

# Auch wenn wir Logs nicht aktualisieren, braucht unsere CRUDBase-Struktur dieses Schema.
class AssetLogUpdate(BaseModel):
    pass

class AssetLog(AssetLogBase):
    id: int
    timestamp: datetime
    changed_by_user_id: int
    changed_by_user: User  # Zeigt den vollständigen Benutzer im Log an

    class Config:
        from_attributes = True