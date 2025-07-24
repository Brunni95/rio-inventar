# Datei: backend/app/crud/manufacturer.py
from app.crud.base import CRUDBase
from app.models import Manufacturer
from app.schemas import ManufacturerCreate, ManufacturerUpdate

class CRUDManufacturer(CRUDBase[Manufacturer, ManufacturerCreate, ManufacturerUpdate]):
    # Hier können später modellspezifische CRUD-Methoden hinzugefügt werden.
    pass

# Wichtig: Erstelle eine Instanz, die in der API verwendet wird.
manufacturer = CRUDManufacturer(Manufacturer)
