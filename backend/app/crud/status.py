# Datei: backend/app/crud/status.py
from app.crud.base import CRUDBase
from app.models import Status
from app.schemas import StatusCreate, StatusUpdate

class CRUDStatus(CRUDBase[Status, StatusCreate, StatusUpdate]):
    # Hier können später modellspezifische CRUD-Methoden hinzugefügt werden.
    pass

# Wichtig: Erstelle eine Instanz, die in der API verwendet wird.
status = CRUDStatus(Status)
