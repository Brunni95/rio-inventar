from pydantic import BaseModel
from datetime import datetime
from .user import User # Importiere das User-Schema für die Anzeige

class AssetLogBase(BaseModel):
    action: str
    field_changed: str | None = None
    old_value: str | None = None
    new_value: str | None = None
    notes: str | None = None

class AssetLogCreate(AssetLogBase):
    asset_id: int
    changed_by_user_id: int

class AssetLog(AssetLogBase):
    id: int
    timestamp: datetime
    changed_by_user: User # Zeigt den kompletten Benutzer an

    class Config:
        from_attributes = True
