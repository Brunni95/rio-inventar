# Datei: backend/app/crud/location.py
from app.crud.base import CRUDBase
from app.models import Location
from app.schemas import LocationCreate, LocationUpdate

class CRUDLocation(CRUDBase[Location, LocationCreate, LocationUpdate]):
    # Hier können später modellspezifische CRUD-Methoden hinzugefügt werden.
    pass

# Wichtig: Erstelle eine Instanz, die in der API verwendet wird.
location = CRUDLocation(Location)
